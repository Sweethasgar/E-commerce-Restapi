from django.shortcuts import render
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import Product,Review,Category,Carts
from .serializers import (
    Productserializers,
    Userserializer,
    UserProfileserializer,
    ReviewSerializer,
    Cartsserializer,
    CategorySerializer,
    PostProductserializers,
    SimpleReviewSerializer,
    Orderserializer,
)
from django.shortcuts import render,get_object_or_404
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework import authentication, permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }    

class userRegistration(APIView):
   def post(self,request):
    serializer=Userserializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user=serializer.save()
        token=get_tokens_for_user(user)
        return Response({'msg':'successfull','token':token})
    return Response(serializer.errors,status=status.HTTP_204_NO_CONTENT)               
        

class userProfileView(APIView):
    authenticate=[JWTAuthentication]
    permission_classes=[IsAuthenticated] 

    def get(self,request):
        serializer=UserProfileserializer(request.user)
        return Response(serializer.data)




@api_view(["GET"])
def get_routs(request):
    routes=[
        'api/token/',
        'api/token/refresh/'

    ]
    return Response(routes,)


class ProductView(APIView):
    # authenticate=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]    
    # permissions_classes = [permissions.IsAuthenticated]
    def get(self,request):
        product= Product.objects.all()
        serializer=PostProductserializers(product,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=PostProductserializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



class  ProductDetailView(APIView):
    def get(self,request,pk):
        product= get_object_or_404(Product,id=pk)
        serializer=Productserializers(product)
        return Response(serializer.data)

    def put(self,request,pk):
        product=get_object_or_404(Product,id=pk)
        serializer=Productserializers(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self,request,pk):
        products=get_object_or_404(Product,id=pk)
        products.delete()
        return Response({"msg:deleted"},status=status.HTTP_204_NO_CONTENT)    
        
class ProductModelView(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=PostProductserializers
    filter_backends= [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class=ProductFilter
    search_fields=['name']
    ordering_fields=['price']
    pagination_class=PageNumberPagination


class CategoryView(ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer


class ReviewView(ModelViewSet):
    queryset=Product.objects.all()
    permission_classes=[IsAuthenticated]
    @action(methods=["get"], detail=True)
    def get_review(self,request,pk):
        product=get_object_or_404(Product,id=pk)
        reviews=product.review_set.all()
        serializer=ReviewSerializer(reviews,many=True)
        return Response(serializer.data)
    @action(methods=["post"], detail=True)
    def post_review(self,request,pk):
        user=request.user
        product=get_object_or_404(Product,id=pk) 
        serializer=ReviewSerializer(data=request.data,context={"user":user,"product":product})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)   
# OR

class ReviewViewApi(APIView):
    authenticate=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
   
    def get(self,request,pk):
        product=get_object_or_404(Product,id=pk)
        reviews=product.review.all()
        serializer=ReviewSerializer(reviews,many=True)
        return Response(serializer.data)
   
    def post(self,request,pk):
        user=request.user
        product=get_object_or_404(Product,id=pk) 
        serializer=ReviewSerializer(data=request.data,context={"user":user,"product":product})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self,request,pk):
        try:
            user=request.user
            review=user.review_set.get(id=pk)
            product=review.product
            serializer=SimpleReviewSerializer(review,request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user,product=product)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class CartApiView(ModelViewSet):

    @action(methods=["post"],detail=True)
    def add_to_cart(self,request,pk):
        user=request.user
        product=get_object_or_404(Product,id=pk)
        serializer=Cartsserializer(data=request.data,context={'user':user,'product':product})
        serializer.is_valid(raise_exception=True)
        try:
            cart=Carts.objects.get(user=user,product=product)
            cart.quntity+= 1
            cart.save()
            return Response({"msg":"succes"})

        except:
            serializer.save(user=user,product=product)
            return Response(serializer.data,status=status.HTTP_409_CONFLICT)     


  
    def destroy(self,request,pk)      :
        cart=get_object_or_404(Carts,id=pk)
        cart.delete()
        return Response({"msg:deleted"},status=status.HTTP_204_NO_CONTENT)    


class cartview(APIView):
    def get(self, request, *args, **kwargs):
        qs=Carts.objects.filter(user=request.user)
        serializer=Cartsserializer(qs,many=True)
        return Response(serializer.data)



class cartviewsss(ModelViewSet):
    serializer_class = Cartsserializer
    queryset = Carts.objects.all()
    # authentication_classes = [authentication.TokenAuthentication]

    def list(self, request, *args, **kwargs):
        qs=Carts.objects.filter(user=request.user)
        serializer=Cartsserializer(qs,many=True)
        return Response(data=serializer.data)
    def create(self, request, *args, **kwargs):
        return Response(data={"msg":"no acces"})



class OrdersView(APIView):
    def post(self,request,pk):
        user=request.user
        product=get_object_or_404(Product,id=pk)
        serializer=Orderserializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product,user=user)
        cart=user.carts_set.filter(product=product).first()
        cart.delete()
        return Response(serializer.data)


        