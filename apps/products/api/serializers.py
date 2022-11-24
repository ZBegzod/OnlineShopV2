from rest_framework import serializers
from apps.products.models import *


class ProductImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImages
        fields = ['images']


class ProductSerializer(serializers.ModelSerializer):

    color = serializers.StringRelatedField(many=True)
    size = serializers.StringRelatedField(many=True)

    product_images = ProductImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['name', 'model', 'made_of_type',
                  'color', 'size', 'description',
                  'price', 'product_order_type',
                  'image', 'product_images']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name', 'image']


class FashionProductModelSerializer(serializers.ModelSerializer):

    product = ProductSerializer(many=True)

    class Meta:
        model = FashionProduct
        fields = '__all__'


class NewProductModelSerializer(serializers.ModelSerializer):

    product = ProductSerializer(many=True)

    class Meta:
        model = NewProduct
        fields = '__all__'


class SaleProductModelSerializer(serializers.ModelSerializer):

    product = ProductSerializer(many=True)

    class Meta:
        model = SaleProduct
        fields = '__all__'


class CategoryProductSerializer(serializers.ModelSerializer):

    category_products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):

    collection_products = ProductSerializer(many=True, read_only=True)

    class Meta:

        model = Collection
        fields = '__all__'


