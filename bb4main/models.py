from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class FoodItem(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    expiry_date = models.DateField()
            
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

