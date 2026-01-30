from django.shortcuts import render
from django.db.models import Max
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from .tasks import send_order_confirmation_email
# from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Product
from .serializer import *
from .filters import ProductFilter, IsStockFilterBackend, OrderFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class CreateProductAPIList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
        IsStockFilterBackend
    ]
    search_fields = ['name', 'description',]
    @method_decorator(cache_page(60 * 5, key_prefix="product_list"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    def get_queryset(self):
        import time
        time.sleep(3)
        return super().get_queryset()
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    
class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class ProductInfoApiView(APIView):
    def get(self, request):
        products = Product.objects.all()
        item_count =  len(products)
        max_price = products.aggregate(max_price=Max('price'))['max_price']
        
        serializers = ProductInfoserializer({
            'products':products,
            'item_count':item_count,
            'max_price':max_price
        })
        return Response(serializers.data)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product').all()
    serializer_class = OrderSerializer
    pagination_class = None
    filterset_class = OrderFilter
    permission_classes=[IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    
    
    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def get_serializer_class(self):
        import time
        time.sleep(3)
        if self.action == "create" or self.action == "update":
            return OrderCreateSerialzer
        return super().get_serializer_class()
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user= self.request.user)
        return qs
    
    def perform_create(self, serializer):
        order = serializer.save(user = self.request.user)
        send_order_confirmation_email.delay(order.order_id, self.request.user.email)
    
    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.request.method == "DELETE":
            self.permission_classes=[IsAdminUser]
        return super().get_permissions()
        
    
