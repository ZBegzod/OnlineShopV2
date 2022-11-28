from django.urls import path
from rest_framework import routers
from apps.products.api.viewset import *

router = routers.DefaultRouter()

router.register(r'collections', CollectionViewSet, basename='collections')  # collections for main and for meny page
router.register(r'categories', CategoryViewSet, basename='categories')  # categories for main  and for meny page
router.register(r'catalog-products', ProductFilterViewSet, basename='catalog-products')  # filter for products
router.register(r'search-products', ProductFilterBySexViewSet, basename='fashions-products')  # fash products for main page
router.register(r'fashion-products', FashionProductViewSet, basename='fashions-products')  # fash products for main page
router.register(r'sale-products', SaleProductViewSet, basename='sale-products')  # sale products for main page
router.register(r'new_products', NewProductViewSet, basename='new-products')  # new products for main page

urlpatterns = router.urls

