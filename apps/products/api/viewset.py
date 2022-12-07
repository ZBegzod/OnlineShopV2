from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, mixins
from apps.products.api.serializers import *
from apps.products.api.filters import *
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from .permissions import IsOwner
from rest_framework.exceptions import (
    NotAcceptable
)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly)
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveDestroyAPIView,
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


class ProductFilterViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    permission_classes = [IsAuthenticatedOrReadOnly]


class FashionProductViewSet(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    queryset = FashionProduct.objects.all()
    serializer_class = FashionProductModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SaleProductViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = SaleProduct.objects.all()
    serializer_class = SaleProductModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class NewProductViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = NewProduct.objects.all()
    serializer_class = NewProductModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CartListApiView(ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsOwner, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Cart.objects.filter(customer=user)
        return queryset


class CartCreateApiView(CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = None
    permission_classes = [IsOwner, IsAuthenticated]

    def post(self, request, *args, **kwargs):

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


@api_view(['GET'])
@login_required(login_url='accounts-api/login/')
@permission_classes([IsOwner, IsAuthenticated])
def my_cart_view(request):
    categories = Category.objects.all()
    cart, cart = Cart.objects.get_or_create(customer=request.user)
    data = {
        'categories': categories,
        'cart': cart
    }
    return JsonResponse(data, status=200)


@api_view(['POST'])
@permission_classes([IsOwner, IsAuthenticated])
def plus_quantity(request):
    cart_item_id = request.GET.get('cart_item_id')

    cart_item = CartItem.objects.get(id=cart_item_id)
    if cart_item.product.available_inventory < cart_item.quantity:
        raise NotAcceptable('We do not have enough inventory of ' + str(cart_item.product.title) +
                            'to complete your purchase. Sorry, we will restock soon')
    cart_item.quantity += 1
    cart_item.product.available_inventory -= 1
    cart_item.product.save()
    cart_item.save()

    data = {'success': True, 'message': 'cart item incremented by one', 'cart_item': cart_item.get_total}
    return JsonResponse(data, status=200)


@api_view(['POST'])
@permission_classes([IsOwner, IsAuthenticated])
def minus_quantity(request):
    cart_id = request.GET.get('cart_id')
    cart_item = CartItem.objects.get(id=cart_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.product.available_inventory += 1
        cart_item.product.save()
        cart_item.save()
        data = {
            'success': True,
            'message': 'cart item decremented by one'
        }
    else:
        cart_item.delete()
        data = {
            'success': True,
            'deleted': True,
            'message': 'cart item was deleted'
        }
    return JsonResponse(data, status=200)


@api_view(['POST'])
@permission_classes([IsOwner, IsAuthenticated])
def delete_cart_item_view(request):
    cart_id = request.GET.get('cart_id')
    cart_item = CartItem.objects.get(id=cart_id)
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
    permission_classes = [IsOwner, IsAuthenticated]

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


