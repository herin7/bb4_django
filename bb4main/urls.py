from django.urls import path,include
from . import views

urlpatterns = [
     path("add/",views.add_food_item,name='add_food_item'),
     path("view/",views.view_food_items,name='view_food_items'),
     path('accounts/', include('allauth.urls')),
     path("logout",views.logout_view),
     path("",views.home)
]
     