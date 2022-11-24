from django.db import models
from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.


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
    price = models.IntegerField(default=0)

    PRODUCT_ORDER_TYPE = [

        ('sale', 'Sale'),
        ('new', 'New'),
        ('fashion', 'Fashion'),
    ]

    product_order_type = models.CharField(max_length=150, choices=PRODUCT_ORDER_TYPE)
    image = models.ImageField(upload_to='product/images')

    def __str__(self):
        return f'{self.name}'


class SaleProduct(models.Model):

    product = models.ManyToManyField(Product, related_name='sale_products')
    images = models.ImageField(upload_to='sale/images')

    def __str__(self):
        return f"{self.product}"


class FashionProduct(models.Model):

    product = models.ManyToManyField(Product, related_name='fashion_products')
    images = models.ImageField(upload_to='fashion/images')

    def __str__(self):
        return f"{self.product}"


class NewProduct(models.Model):

    product = models.ManyToManyField(Product, related_name='new_products')
    images = models.ImageField(upload_to='new/images')

    def __str__(self):
        return f"{self.product}"


class ProductImages(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    images = models.ImageField(upload_to='product/images')

    def __str__(self):
        return f'{self.product}'


class Order(models.Model):

    products = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    count = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.products}'
