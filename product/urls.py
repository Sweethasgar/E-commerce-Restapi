from django.urls import path
from . import views
from product import views
from.views import MyTokenObtainPairView
from product.views import userRegistration,userProfileView,ProductModelView,ReviewViewApi,CartApiView,cartview,cartviewsss,OrdersView
from rest_framework_simplejwt.views import (
  
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register("products/all",views.ProductModelView)
router.register("category",views.CategoryView,basename="review"),
router.register("cart", views.CartApiView,basename="cart")
router.register("items/cart", views.cartviewsss,basename="items")
# router.register("reviews",views.ReviewView,basename="review"),




urlpatterns=[
    path("",views.get_routs),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path("signup",userRegistration.as_view()),
    path("profile",views.userProfileView.as_view()),
    path("products",views.ProductView.as_view()),
    path("products/<str:pk>",views.ProductDetailView.as_view()),
    path("view/<str:pk>",views.ReviewViewApi.as_view()), 
    path("orders/<str:pk>",views.OrdersView.as_view()),
     
   
    # path("items",views.cartview.as_view()),
]+router.urls


#   path("signup",userRegistration.as_view()),==>user registration
#   router.register("category",views.CategoryView,basename="review"),==>add category
#   path("products",views.ProductView.as_view()),==>view product and add product
#   path("products/<str:pk>",views.ProductDetailView.as_view()),==> single product(view, update , delete)
#   router.register("category",views.CategoryView,basename="review"),==> to view and add new category
#   path("view/<str:pk>",views.ReviewViewApi.as_view()), ==>to add review,get particular product review and update review
#   router.register("cart", views.CartApiView,basename="cart")(call add to cart) ==>to add and delete cart
#   router.register("items/cart", views.cartviewsss,basename="items")==> to view a user Cart