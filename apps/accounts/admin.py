from django.contrib import admin

# Register your models here.
from apps.accounts.models import *

admin.site.register(CustomUser)
