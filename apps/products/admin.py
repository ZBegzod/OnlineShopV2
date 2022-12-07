from django.contrib import admin

# Register your models here.
from apps.products.models import *

admin.site.register(Category)
admin.site.register(Collection)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Product)
admin.site.register(ProductImages)
admin.site.register(FashionProduct)
admin.site.register(NewProduct)
admin.site.register(SaleProduct)

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)




