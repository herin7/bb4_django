from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime
from .models import FoodItem
import os
import google.generativeai as genai
from google.generativeai import GenerativeModel
import configparser


# Read API key from the configuration file
config = configparser.ConfigParser()
config.read('config.private.ini')
api_key = config['GENAI']['API_KEY']
credentials_file_path = config['GENAI']['CREDENTIALS_FILE_PATH']


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_file_path

genai.configure(api_key=os.getenv("API_KEY"))
generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
model = genai.GenerativeModel("gemini-pro", generation_config=generation_config)

def home(request):
    return render(request, 'layout.html')

def logout_user(request):
    logout(request)
    return render(request, 'layout.html')

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

        return redirect('view_food_items')  # Redirect to a success page
    return render(request, 'add_food_item.html')

@login_required
def chat_bot(request):
    user_input = request.POST.get('user-input', '')
    food_items = FoodItem.objects.filter(user=request.user)
    food_item_details = "\n".join([f"{item.product_name} - Quantity: {item.quantity}, Expiry Date: {item.expiry_date}" for item in food_items])
    merged_input = user_input + "\n\nList of your food items:\n" + food_item_details
    default_input = "Answer user's question only after analyzing the food items."
       # Define a detailed default prompt for developers
    developer_prompt = ("Ensure that the You provides informative responses based on user inquiries related to "
                    "food inventory management. Analyze user input to provide relevant details about food items, such as "
                    "quantity, expiry date, and any other relevant information. Strive to assist users in managing their "
                    "inventory efficiently by offering accurate and helpful responses to their queries.")
    
    merged_input += "\n\n" + default_input + "\n\n" + developer_prompt
    response = model.generate_content([merged_input])
    chatbot_response = response.text
    return render(request, 'chatbot.html', {'response': chatbot_response})