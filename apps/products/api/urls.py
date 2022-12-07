from django.urls import path
from rest_framework import routers
from apps.products.api.viewset import *

router = routers.DefaultRouter()

router.register(r'collections', CollectionViewSet, basename='collections')  # collections for main and for meny page
router.register(r'categories', CategoryViewSet, basename='categories')  # categories for main  and for meny page
router.register(r'catalog-products', ProductViewSet, basename='catalog-products')  # filter for products
router.register(r'fashion-products', FashionProductViewSet, basename='fashions-products')  # fash products for main page
router.register(r'sale-products', SaleProductViewSet, basename='sale-products')  # sale products for main page
router.register(r'new_products', NewProductViewSet, basename='new-products')  # new products for main page

urlpatterns = router.urls

urlpatterns += [

    # cart
    path('cart', CartListApiView.as_view(), name='cart'),
    path('cart-create', CartCreateApiView.as_view(), name='cart-create'),
    path('cart-by-category', my_cart_view, name='cart-by-category'),
    path('plus-quantity', plus_quantity, name='plus-quantity'),
    path('minus-quantity', minus_quantity, name='minus-quantity'),
    path('cart-delete', delete_cart_item_view, name='cart-delete'),

    # order
    path("order/", OrderListApiView.as_view(), name='order'),
    path("order/", OrderCreateAPIView.as_view(), name='order'),

]
