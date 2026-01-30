from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('orders', views.OrderViewSet, 'orders')
urlpatterns = [
    
    path('users/', views.UserListView.as_view(), name='users'),
    path('products/', views.CreateProductAPIList.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetailAPIView.as_view(), name='product-details'),
    path('products/info/', views.ProductInfoApiView.as_view(), name='product_info'),
    # path('orders/', OrderListAPIView.as_view(), name='order_details'),
    # path('user/orders/', UserOrderListAPIView.as_view())

]


urlpatterns += router.urls
