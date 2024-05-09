from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import FoodItem


@receiver(post_save, sender=FoodItem)
def notify_expiry(sender, instance, **kwargs):
    if instance.expiry_date <= timezone.now().date():
        subject = f"Food Item Expired: {instance.product_name}"
        message = f"Hello {instance.user.username},\n\nYour food item '{instance.product_name}' has expired. Please consider removing it from your inventory."
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.user.email]

        send_mail(subject, message, from_email, recipient_list)