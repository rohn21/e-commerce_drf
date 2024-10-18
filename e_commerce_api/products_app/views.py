from django.shortcuts import render
from products_app.serializers import ProductSerializer, CustomerSerializer, OrderSerializer, OrderItemSerializer
from products_app.models import Customer, Product, Order, OrderItem
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

class CustomerListView(ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
class CustomerDetailview(RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ProductListView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class ProductDetailview(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class OrderListView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        customers_name = self.request.query_params.get('customers', None)
        product_name = self.request.query_params.get('products', None)
        
        if product_name:
            product_name = product_name.split(',')
            queryset = queryset.filter(orderitem__product__name__in=product_name).distinct()
            
        if customers_name:
            customers_name = customers_name.split(',')
            queryset = queryset.filter(customer__name__in=customers_name)
            
        return queryset

class OrderDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer