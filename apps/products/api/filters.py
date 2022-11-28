import django_filters as filters
from apps.products.models import *


class ProductFilter(filters.FilterSet):

    price = filters.NumberFilter(field_name='price', lookup_expr='gte')

    class Meta:
        model = Product
        fields = ['color', 'size', 'price']


class ProductSexFilter(filters.FilterSet):

    class Meta:
        model = Product
        fields = ['filter_by_sex']

