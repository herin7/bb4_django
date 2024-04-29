from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class FoodItem(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None)
    product_name = models.CharField(max_length=100, default=None)
    product_type = models.CharField(max_length=50, default=None)
    quantity = models.IntegerField()
    expiry_date = models.DateField()

    def __str__(self):
        return self.product_name  


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

