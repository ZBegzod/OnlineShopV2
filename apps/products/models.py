from django.db import models
from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.


class Category(models.Model):

    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='category/images')

    def __str__(self):
        return f'{self.name}'


class Color(models.Model):

    color = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.color}'


class Size(models.Model):

    size = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.size}'


class Product(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    model = models.CharField(max_length=140)
    made_of_type = models.CharField(max_length=200)
    color = models.ManyToManyField(Color)
    size = models.ManyToManyField(Size)
    description = RichTextField(null=True, default='')

    PRODUCT_ORDER_TYPE = [

        ('sale', 'Sale'),
        ('new', 'New'),
        ('fashion', 'Fashion'),
    ]

    product_order_type = models.CharField(choices=PRODUCT_ORDER_TYPE)
    image = models.ImageField(upload_to='product/images')

    def __str__(self):
        return f'{self.name}'


class Collection(models.Model):

    title = models.CharField(max_length=120)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='product/images')

    def __str__(self):
        return f'{self.title}'


class Order(models.Model):

    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL)
    count = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.collection}'
