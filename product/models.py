from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import timedelta,date


# Create your models here.

class Category(models.Model):
    title=models.CharField(max_length=150)

    def __str__(self):
        return self.title


class Product(models.Model):
    name=models.CharField(max_length=100)
    description= models.CharField(max_length=100)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    price=models.IntegerField(default=0)
    inventory=models.IntegerField(default=1)
    
    def __str__(self):
        return self.name

    def review(self):
        return self.review_set.all().count()

class Review(models.Model):
    user=models.ForeignKey(User(), on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE,related_name='review')
    Review=models.CharField(max_length=150)
    rating=models.FloatField(validators=[MinValueValidator(1),MinValueValidator(5)])      

    def __str__(self):
        return self.Review  


class Carts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    qty = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1), MaxValueValidator(10)])
    options = (
        ("in cart", "in cart"),
        ("order_placed", "order_placed"),
        ("cancelled", "cancelled"),

    )
    status = models.CharField(max_length=12, choices=options, default="in cart")        




class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    orderdate = models.DateField(auto_now_add=True, null=True)
    expected_date=models.CharField(max_length=150)
    options = (
        ("order_placed", "order_placed"),
        ("delivered", "delivered")
    )
    status = models.CharField(max_length=20, choices=options, default="order_placed")
    