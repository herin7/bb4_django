from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import FoodItemForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime
from .models import FoodItem

def home(request):
    return render(request, 'home.html')



def logout_view(request):
    logout(request)
    return redirect("/")



@login_required
def view_food_items(request):
    food_items = FoodItem.objects.all()
    return render(request,'view_food_items.html', {'food_items' : food_items})






@login_required
def save_fooditem(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_type = request.POST.get('product_type')
        quantity = request.POST.get('quantity')
        expiry_date = request.POST.get('expiry_date')
        
        fooditem = FoodItem.objects.create(user=request.user, product_name=product_name, product_type=product_type, quantity=quantity, expiry_date=expiry_date)
        
        
        return redirect('view_food_items')  # Redirect to a success page
    return render(request, 'add_food_item.html')


def fillter(request):
    now=datetime.datetime.now()
    food_items = FoodItem.objects.expiry_date
    return render(request, "view_food_items.html",{
        "current": now.year >  food_items.year
    })