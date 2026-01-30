from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import *

#Create your tests here.
class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')
        self.normal_user = User.objects.create_user(username='user', password='userpass')
        self.product = Product.objects.create(
            name = "Test Product",
            price = 300.00,
            stock = 14,
            description = "Test Description"
        )
        
        self.url = reverse('product-details', args=[self.product.pk])
        
    def test_get_product(self):
        response = self.client.get(self.url,)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)
    
    def test_unauthorized_update_product(self):
        data = {'name':'update_product'}
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_normal_user_update_product(self):
        self.client.login(username='user', password='userpass')
        data = {'name':'update_product'}
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_unauthorized_delete_product(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_only_admin_can_delete_product(self):
        #test normal user
        self.client.login(username='user', password='userpass')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())
        
        #test admin user
        self.client.login(username='admin', password='adminpass')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())
        
class OrderAPITestCase(APITestCase):
    
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')
        self.normal_user = User.objects.create_user(username='user', password='userpass')
        self.url1 = reverse('orders-list')
        self.product1 = Product.objects.create(
            name="P1", price=100, stock=10
        )
        self.product2 = Product.objects.create(
            name="P2", price=200, stock=5
        )
        self.order = Order.objects.create(
            user=self.normal_user,
            status="Confirm"
        )

        self.url2 = reverse('orders-detail', args=[self.order.pk])
        
    def test_order_product_as_anonymous_user(self):
        order = {
            "items": [
                {"product": self.product1.id, "quantity": 3},
                {"product": self.product2.id, "quantity": 2},
            ]
        }
        response = self.client.post(self.url1, order, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_normal_user_can_delete_order(self):
        self.client.login(username='user', password='userpass')
        response = self.client.delete(self.url2)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Order.objects.filter(pk=self.order.pk).exists())
    
    def test_normal_user_can_delete_order(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.delete(self.url2)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(pk=self.order.pk).exists())