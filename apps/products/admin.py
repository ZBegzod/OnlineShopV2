from django.contrib import admin
from apps.products.models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Collection)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Product)
admin.site.register(ProductImages)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)




