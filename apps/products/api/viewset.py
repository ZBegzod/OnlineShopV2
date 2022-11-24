from rest_framework import viewsets, mixins
from apps.products.api.serializers import *
from apps.products.models import *
from apps.products.api.filters import *


class CollectionViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class FashionProductViewSet(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter


class SaleProductViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = SaleProduct.objects.all()
    serializer_class = SaleProductModelSerializer


class NewProductViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = NewProduct.objects.all()
    serializer_class = NewProductModelSerializer

