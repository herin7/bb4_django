from django.urls import path,include
from . import views

urlpatterns = [
     path("add/",views.save_fooditem,name='save_fooditem'),
     path("view/",views.view_food_items,name='view_food_items'),
     path('accounts/', include('allauth.urls')),
      path('logout/', views.logout_view, name='logout'),
     path("",views.home),
     path("chat/",views.chatbot,name='chatbot'),
   
   
]