
from django.http import JsonResponse
from rest_framework import serializers, status, viewsets, fields
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from rest_framework.pagination import PageNumberPagination


from myapp.models import *

from .serializers import *

#Serializer for users
MIN_LENGTH = 8

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        write_only=True,
        min_length=MIN_LENGTH,
        error_messages={
            "min_length": f"Password must be longer than  {MIN_LENGTH} characters."
        }
    )
    
    password2 = serializers.CharField(
        write_only=True,
        min_length=MIN_LENGTH,
        error_messages={
            "min_length": f"Password must be longer than  {MIN_LENGTH} characters."
        }
    )
    
    class Meta:
        model = User
        fields = ["id", "username", "password", "password2", "first_name", "last_name", "email", "is_superuser", "is_staff", "is_active"]
        
    def validate(self, data):
        if data["password"] != data ["password2"]:
            raise serializers.ValidationError("Password does not match.")
        return data
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        
        user.set_password(validated_data["password"])
        user.save()
        
        return user

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = {AllowAny}
    queryset = User.objects.all()
    serializer_class =  UserSerializer
    
class UserDetails(viewsets.ModelViewSet):
    permission_classes = {IsAdminUser, }
    serializer_class = UserSerializers
    queryset = User.objects.all()
        
class collectionsView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    serializer = CategorySerializer(queryset, many = True)
    
    
class productView(viewsets.ModelViewSet):
    queryset = product.objects.all()
    serializer_class = productSerializer
    serializer = productSerializer(queryset, many = True)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']
    pagination_class = PageNumberPagination
    
class cartView(viewsets.ModelViewSet):
    permission_classes = {AllowAny}
    queryset = Cart.objects.all()
    serializer_class = CartSerializer   
    
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = {IsAuthenticated}
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    
class OrderItemViewSet(viewsets.ModelViewSet):
    permission_classes = {IsAuthenticated}
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    
    
    
    