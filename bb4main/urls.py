from django.urls import path
from . import views

urlpatterns = [
    
     path("logout",views.logout_view),
     path("",views.home)
]