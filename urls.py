from django.contrib import admin
from django.urls import include, path
from django.conf.urls import include


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
#to register an account
router.register("register", views.UserViewSet, basename="register"),
router.register("user", views.UserDetails, basename="user"),
router.register("category", views.collectionsView, basename="category"),
router.register("product", views.productView, basename="product"),
router.register("cart", views.cartView, basename="cart"),
router.register("orderitem", views.OrderItemViewSet, basename="orderitem"),
router.register("order", views.OrderViewSet, basename="order"),


urlpatterns = [
    path("api-auth", include('rest_framework.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]


urlpatterns += router.urls

