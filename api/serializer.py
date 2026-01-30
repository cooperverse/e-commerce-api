from rest_framework import serializers
from django.db import transaction
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "get_full_name", "email", "orders"]
class ProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = Product
        fields = ('product_id','name', 'description', 'price', 'stock')
        
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be a non-negative value.")
        return value
    
    
        
class ProductInfoserializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    item_count = serializers.IntegerField()
    
    

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.CharField(source='product.price', read_only=True)

    
    class Meta:
        model = OrderItem
        fields = ('product_name','quantity', 'product_price', 'item_subtotal')
        

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    
    def get_total_price(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)
    
    class Meta:
        model = Order
        fields = ('order_id','created_at','user','status','items', 'total_price')
        
        
class OrderCreateSerialzer(serializers.ModelSerializer):
    class CreateOrderItemSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ['product', 'quantity']
    items = CreateOrderItemSerializer(many = True, required=False)
    order_id = serializers.UUIDField(read_only = True)
    class Meta:
        model = Order
        fields = ['user',  'status', 'order_id','items' ]
        extra_kwargs = {
            'user':{'read_only':True}
        } 
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            for items in items_data:
                OrderItem.objects.create(order=order, **items)
        
        return order 
    def update(self, instance, validated_data):
        orderitems_data = validated_data.pop('items')
        with transaction.atomic():
            instance = super().update(instance, validated_data)
            
            if orderitems_data is not None:
                instance.items.all().delete()
                
                for items in orderitems_data:
                    OrderItem.objects.create(order=instance, **items )
        return instance

