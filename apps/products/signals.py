from .models import *
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_cart_item(sender, created, instance, *args, **kwargs):
    if created:
        Cart.objects.create(customer=instance)
