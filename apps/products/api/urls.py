from rest_framework import routers
from django.urls import path
from apps.products.api.viewset import *

router = routers.DefaultRouter()

router.register(r'collections', CollectionViewSet, basename='collections')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'fashion-products', FashionProductViewSet, basename='fashions-product')
router.register(r'sale-products', SaleProductViewSet, basename='sale-product')
router.register(r'new_products', NewProductViewSet, basename='new-product')

urlpatterns = router.urls

