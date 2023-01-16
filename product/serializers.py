from rest_framework import serializers
from . models import Product,Review,Category,Carts,Orders
from djoser.serializers import UserCreateSerializer
from django.contrib.auth.models import User


class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
                  "username",
                  "email",
                  "password"
                  ]

        extra_kwargs={
                       'email':{"required":True}
                  }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

# or

class UserProfileserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
                 'id',
                  "username",
                  "email",
                  ]
                   
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=[
            "id","title"
        ]    

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields='__all__'

class Productserializers(serializers.ModelSerializer):
    # category=serializers.CharField(source="category.title",read_only=True)
    
    class Meta:
        model=Product
        fields=[
           "id", "name","description","category","price","inventory","review"
        ]

    category=CategorySerializer()  
    review = ReviewSerializer(many=True,read_only=True)


class PostProductserializers(serializers.ModelSerializer):
    # category=serializers.CharField(source="category.title",read_only=True)
    
    class Meta:
        model=Product
        fields=[
           "id", "name","description","category","price","inventory",
        ]
   
     

    
class ReviewSerializer(serializers.ModelSerializer):
    user= serializers.CharField(read_only=True)
    product = serializers.CharField(read_only=True)
    class Meta:
        model=Review
        fields='__all__'
     
    
    def create(self, validated_data):
        user=self.context.get("user")
        product=self.context.get("product")
        return Review.objects.create(user=user,product=product,**validated_data)



class SimpleReviewSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    product=serializers.CharField(read_only=True)
    class Meta:
        model=Review
        fields='__all__'
    
class Cartsserializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    product = serializers.CharField(read_only=True)
    date = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
  

    class Meta:
        model=Carts
        fields = [
            "id",
            "user",
            "product",
            "date",
            "qty",
            "status"
        ]

    # def create(self, validated_data):
    #     user = self.context.get("user")
    #     product = self.context.get("product")
    #     return Carts.objects.create( user=user, product=product,**validated_data)    


class Orderserializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    product = serializers.CharField(read_only=True)
    class Meta:
        model=Orders
        fields="__all__"