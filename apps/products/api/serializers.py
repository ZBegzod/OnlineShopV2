from rest_framework import serializers
from apps.products.models import *
from apps.accounts.models import CustomUser


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['id', 'images']


class ProductSerializer(serializers.ModelSerializer):
    color = serializers.StringRelatedField(many=True)
    size = serializers.StringRelatedField(many=True)
    product_images = ProductImagesSerializer(many=True, read_only=True)

    # category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'model', 'made_of_type',
                  'color', 'size', 'description',
                  'price', 'image', 'product_images',
                  'category', 'collection']


class CategorySerializer(serializers.ModelSerializer):
    category_products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ['name', 'image', 'category_products']


class CollectionSerializer(serializers.ModelSerializer):
    collection_products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ['title', 'collection_products']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)

    class Meta:
        model = CartItem
        fields = (
            'id',
            'product',
            'quantity',
            'get_total_price'
        )


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    customer = UserSerializer(required=False, read_only=True)

    class Meta:
        model = Cart
        fields = (
            'created_at', 'updated_at', 'items',
            'get_cart_total_count', 'get_cart_total_price',
            'calculated_total_discount', "customer"
        )


class OrderSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = (
            'transaction_id', 'cart', 'customer',
            'order_type', 'order_number',
            'created_at', 'updated_at',
        )
        extra_kwargs = {
            'transaction_id': {"read_only": True},
            'cart': {"required": False},
            'customer': {"required": False},
        }

