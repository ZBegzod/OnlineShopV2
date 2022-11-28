from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class CustomUser(AbstractUser, PermissionsMixin):
    phone_number = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.username}"
