from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.files.storage import default_storage
import pytesseract
from datetime import datetime, timedelta
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms  
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import FoodItem
from django.utils import timezone
import os
import google.generativeai as genai
import configparser
from PIL import Image
from datetime import datetime,date
from datetime import date
import json
from datetime import datetime, timedelta
from datetime import datetime
from django.urls import reverse 
from django.contrib.auth.signals import user_logged_in
from allauth.account.signals import user_logged_in as social_user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import FoodItem
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm  # Import your custom login form
import datetime


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'login.html'  

config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['GENAI']['API_KEY']
credentials_file_path = config['GENAI']['CREDENTIALS_FILE_PATH']

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_file_path

genai.configure(api_key=os.getenv("API_KEY"))
generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
model = genai.GenerativeModel("gemini-1.5-pro-latest", generation_config=generation_config)

def home(request):
    return render(request, 'home.html')

def logout_user(request):
    logout(request)
    return render(request, 'home.html')

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(('view_food_items'))
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')
    

def registration_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            send_welcome_email(user)
            return redirect('home') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration.html', {'form': form})

@login_required
def view_food_items(request):
    food_items = FoodItem.objects.filter(user=request.user)
    expired_food_items = [item for item in food_items if item.expiry_date < datetime.date.today()]
    return render(request, 'view_food_items.html', {'food_items': food_items, 'expired_food_items': expired_food_items})

@login_required
def save_food_item(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_type = request.POST.get('product_type')
        quantity = request.POST.get('quantity')
        expiry_date = request.POST.get('expiry_date')

        fooditem = FoodItem.objects.create(user=request.user, product_name=product_name, product_type=product_type, quantity=quantity, expiry_date=expiry_date)

        return redirect('view_food_items')  
    return render(request, 'add_food_item.html')

@login_required
def chat_bot(request):
    user_input = request.POST.get('user-input', '')
    food_items = FoodItem.objects.filter(user=request.user)
    food_item_details = "\n".join([f"{item.product_name} - Quantity: {item.quantity}, Expiry Date: {item.expiry_date}" for item in food_items])
    merged_input = user_input + "\n\nList of your food items:\n" + food_item_details
    default_input = "Answer user's question only after analyzing the food items."
   
    developer_prompt = ("Ensure that the You provides informative responses based on user inquiries related to "
                    "food inventory management. Analyze user input to provide relevant details about food items, such as "
                    "quantity, expiry date, and any other relevant information. Strive to assist users in managing their "
                    "inventory efficiently by offering accurate and helpful responses to their queries."
                    "Don't include [' at the start of response","Add obnly food, medicines or anything that human consumes, avoid adding devices,things etc",)
                    
                    
    
    merged_input += "\n\n" + default_input + "\n\n" + developer_prompt
    response = model.generate_content([merged_input])
    chatbot_response = response.text
    return render(request, 'chatbot.html', {'response': chatbot_response})
def analyze_image_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        
        with default_storage.open('temp_image.jpg', 'wb+') as destination:
            for chunk in uploaded_image.chunks():
                destination.write(chunk)

        img = Image.open('temp_image.jpg')

        model = genai.GenerativeModel('gemini-pro-vision')

        response = model.generate_content(["Generate a Python list of present products in image,Responese should not start with __ [' __ or not end with __']__ inventory efficiently by offering accurate and helpful responses to their queries.Don't include '''   ['  ''' at the start of response ,Add only food, medicines or anything that human consumes, avoid adding devices,things etcdon't use any additional text only name of product is the thing you have to tell nothing else like 'this image is of ' don't do any formalities ,say nothing else,", img], stream=True)
        response.resolve()

        text_content = response.text

        default_storage.delete('temp_image.jpg')

        text_content = text_content.replace("[", "").replace("]", "").replace(",", "")
        product_list = [product.strip() for product in text_content.split() if product.strip()]

        type_mapping = {
            'fruit': ['apple', 'banana', 'pear'],
            'vegetable': ['lettuce', 'tomato', 'cucumber', 'onion', 'bell pepper'],
            'dairy': ['milk', 'cheese'],
            'grain': ['corn', 'bread'],
            'protein': ['egg', 'chicken', 'beef', 'fish']
        }
 
        for product_name in product_list:
            product_type = 'other'
            quantity = 1
            expiry_date = timezone.now().date() + timedelta(days=90)  # Default expiry date 6 months later
            
            for key, values in type_mapping.items():
                if any(value in product_name.lower() for value in values):
                    product_type = key
                    break

            food_item = FoodItem.objects.create(
                user=request.user,
                product_name=product_name,
                product_type=product_type, 
                quantity=quantity,  
                expiry_date=expiry_date.strftime('%Y-%m-%d')  
            )

            food_item.save()

        return HttpResponse('Products saved to database successfully!')
    else:
        return render(request, 'upload_image.html')

@receiver(user_logged_in)
@receiver(social_user_logged_in)
def send_welcome_email(sender, request, user, **kwargs):
    subject = "Welcome to Our Food Inventory System!"
    message = f"Hello {user.username},\n\nWelcome to our food inventory system. We're glad you joined us!"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)





@receiver(post_save, sender=FoodItem)
def notify_expiry(sender, instance, **kwargs):
    expiry_date = instance.expiry_date
    if isinstance(expiry_date, str):
        expiry_date = datetime.datetime.strptime(expiry_date, '%Y-%m-%d').date()  # Change this line
    
    if expiry_date < timezone.now().date():
        subject = f"Food Item Expired: {instance.product_name}"
        message = f"Hello {instance.user.username},\n\nYour food item '{instance.product_name}' has expired. Please consider removing it from your inventory."
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.user.email]

        send_mail(subject, message, from_email, recipient_list)
        



        
        

def delete_food_item(request, item_id):
    food_item = get_object_or_404(FoodItem, pk=item_id)
    food_item.delete()
    return redirect('view_food_items')  
   
 