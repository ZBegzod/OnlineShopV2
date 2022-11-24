import django_filters
import django_filters as filters
from apps.products.models import *
from django import forms


class ProductFilter(filters.FilterSet):

    price = filters.NumberFilter(field_name='price', lookup_expr='gte')

    class Meta:
        model = Product
        fields = ['color', 'size', 'price']


# class FashionProductFilter(filters.FilterSet):
#
#     price = filters.ModelChoiceFilter(queryset=FashionProduct.objects.all(), field_name='price', lookup_expr='gte')
#
#     class Meta:
#         model = FashionProduct
#         fields = ['product.color', 'product.size', 'product.price']
