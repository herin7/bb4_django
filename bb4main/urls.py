from django.urls import path,include
from . import views

urlpatterns = [
     path('accounts/', include('allauth.urls')),
     path('', views.home, name='home'),
     path('add/', views.save_food_item, name='save_food_item'),
     path('view/', views.view_food_items, name='view_food_items'),
     path('logout/', views.logout_user, name='logout'),
     path('chat/', views.chat_bot, name='chatbot'),
     path('analyze/', views.analyze_image_view, name='analyze_image'),

          

    
]

