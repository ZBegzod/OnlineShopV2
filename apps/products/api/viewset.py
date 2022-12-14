from rest_framework import viewsets, mixins
from apps.products.api.serializers import *
from apps.products.api.filters import *
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from .permissions import *
from rest_framework.exceptions import (
    NotAcceptable
)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly)
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.decorators import (
                                       api_view,
                                       permission_classes
                                       )


class CollectionViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProductViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    permission_classes = [IsAuthenticatedOrReadOnly]


class FashionProductViewSet(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Product.objects.filter(product_type='fashion')
        return queryset


class SaleProductViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Product.objects.filter(product_type='sale')
        return queryset


class NewProductViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Product.objects.filter(product_type='new')
        return queryset


class CartListApiView(ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsOwnerCart, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Cart.objects.filter(customer=user)
        return queryset


class CartItemDetailApiView(RetrieveAPIView):
    permission_classes = [IsOwnerCartItem, IsAuthenticated]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    lookup_field = 'pk'


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cart_create(request):

    user = request.user
    product_id = request.data.get('product_id')
    product = Product.objects.filter(id=product_id).first()
    my_cart, new_cart = Cart.objects.get_or_create(customer=user)

    data = None
    if my_cart:
        CartItem.objects.create(product=product, cart=my_cart)
        data = {
            'success': True,
            'product': product.name,
        }

    if new_cart:
        CartItem.objects.create(product=product, cart=new_cart)
        data = {
            'success': True,
            'product': product.name
        }

    return JsonResponse(data, status=201)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def my_cart_view(request):
#     categories = Category.objects.all()
#     cart, cart = Cart.objects.get_or_create(customer=request.user)
#     data = {
#         'categories': categories,
#         'cart': cart
#     }
#     return Response(data, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def plus_quantity(request):
    cart_item_id = request.data.get('cart_item_id')
    cart_item = CartItem.objects.get(id=cart_item_id)
    if cart_item.product.available_inventory < cart_item.quantity:
        raise NotAcceptable('We do not have enough inventory of ' + str(cart_item.product.title) +
                            'to complete your purchase. Sorry, we will restock soon')
    cart_item.quantity += 1
    cart_item.product.available_inventory -= 1
    cart_item.product.save()
    cart_item.save()

    data = {'success': True, 'message': 'cart item incremented by one', 'price': cart_item.get_total_price}
    return JsonResponse(data, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def minus_quantity(request):
    cart_item_id = request.data.get('cart_item_id')
    cart_item = CartItem.objects.get(id=cart_item_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.product.available_inventory += 1
        cart_item.product.save()
        cart_item.save()
        data = {
            'success': True,
            'message': 'cart item decremented by one',
            'price': cart_item.get_total_price,
        }
    else:
        cart_item.delete()
        data = {
            'success': True,
            'deleted': True,
            'message': 'cart item was deleted',
        }
    return JsonResponse(data, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_cart_item_view(request):
    cart_item_id = request.data.get('cart_item_id')
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.product.available_inventory += cart_item.quantity
    cart_item.product.save()
    cart_item.delete()
    data = {
        'success': True,
        'deleted': True,
        'message': 'cart item was deleted'
    }

    return JsonResponse(data, status=200)


class OrderListApiView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrder, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(customer=user)
        return queryset


class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        cart_id = request.data.get('cart_id')
        cart = Cart.objects.filter(id=cart_id).first()
        serializer.is_valid(raise_exception=True)
        serializer.save(customer_id=request.user.id, cart_id=cart.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

