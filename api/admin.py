from django.contrib import admin
from django.contrib.auth.models import User
from .models import *
# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    
class OrderAdmin(admin.ModelAdmin):
    inlines =[
        OrderItemInline
    ]

admin.site.register(Order, OrderAdmin)
admin.site.register(User)
