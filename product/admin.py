from django.contrib import admin
from .models import Product,Review,Category,Carts
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Carts)
