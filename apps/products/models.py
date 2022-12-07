from django.db import models
from ckeditor.fields import RichTextField
from django.conf import settings
import uuid


class Category(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='category/images')

    def __str__(self):
        return f'{self.name}'


class Collection(models.Model):
    title = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.title}'


class Color(models.Model):
    color = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.color}'


class Size(models.Model):
    size = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.size}'


class Product(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_products')
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='collection_products')
    name = models.CharField(max_length=120)
    model = models.CharField(max_length=140)
    made_of_type = models.CharField(max_length=200)
    color = models.ManyToManyField(Color, verbose_name='colors')
    size = models.ManyToManyField(Size, verbose_name='sizes')
    description = RichTextField(null=True, default='')
    price = models.DecimalField(default=0)
    image = models.ImageField(upload_to='product/images')
    product_code = models.CharField(max_length=70)
    available_inventory = models.PositiveIntegerField(default=0)

    FILTER_BY_SEX = [

        ('male', 'Male'),
        ('female', 'Female'),

    ]

    filter_by_sex = models.CharField(max_length=120, choices=FILTER_BY_SEX)

    def __str__(self):
        return f'{self.name}'


class SaleProduct(models.Model):
    product = models.ManyToManyField(Product, related_name='sale_products')

    def __str__(self):
        return f"{self.product}"


class FashionProduct(models.Model):
    product = models.ManyToManyField(Product, related_name='fashion_products')

    def __str__(self):
        return f"{self.product}"


class NewProduct(models.Model):
    product = models.ManyToManyField(Product, related_name='new_products')

    def __str__(self):
        return f"{self.product}"


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    images = models.ImageField(upload_to='product/images')

    def __str__(self):
        return f'{self.product}'


# Order and Cart Models
class Cart(models.Model):

    customer = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='cart',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def calculated_total_discount(self):
        cart_items = self.items.all()
        total_discount = sum([item.calculate_discount for item in cart_items])
        return total_discount

    @property
    def get_cart_total_count(self):
        cart_items = self.items.all()
        total = sum([item.quantity for item in cart_items])
        return total

    @property
    def get_cart_total_price(self):
        cart_items = self.items.all()
        total = sum([item.get_total_price for item in cart_items])
        return total

    def __str__(self):
        return f"{self.customer.username}"


class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        related_name='items',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    product = models.ForeignKey(
        Product,
        related_name='items',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    discount = models.FloatField(null=True, blank=True)

    @property
    def get_total_price(self):
        total = self.quantity * self.product.price
        return total

    @property
    def calculate_discount(self):
        discount = (self.discount * self.product.price)
        return discount

    def __str__(self):
        return f"{self.product.name}"


class Order(models.Model):

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_orders',
        on_delete=models.SET_NULL, null=True
    )

    transaction_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    order_type = models.CharField(max_length=140)
    order_number = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    STATUS = [

        (1, 'Delivered'),
        (2, 'Canceled'),
        (3, 'Process'),

    ]

    status = models.CharField(max_length=120, choices=STATUS)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.cart.customer}"
