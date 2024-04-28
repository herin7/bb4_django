from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import FoodItemForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .models import FoodItem

def home(request):
    return render(request, 'home.html')



def logout_view(request):
    logout(request)
    return redirect("/")



@login_required
def add_food_item(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.user = request.user  
            food_item.save()
            return redirect('view_food_items')
    else:
        form = FoodItemForm()
    return render(request, 'add_food_item.html', {'form': form})


@login_required
def view_food_items(request):
    food_items = FoodItem.objects.all()
    return render(request,'view_food_items.html', {'food_items' : food_items})