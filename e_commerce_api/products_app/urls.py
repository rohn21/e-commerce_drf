from django.urls import path
from products_app.views import (CustomerListView, CustomerDetailview,
                                ProductListView, ProductDetailview,
                                OrderListView, OrderDetailView)

urlpatterns = [
    
    #customers-URLs
    path('customers/', CustomerListView.as_view(), name='create-list-customers'),
    path('customers/<int:pk>/', CustomerDetailview.as_view(), name='customers-details'),
    
    # products-URLs
    path('products/', ProductListView.as_view(), name='create-list-product'),
    path('products/<int:pk>/', ProductDetailview.as_view(), name='products-details'),
    
    # orders-and-orderItem-URLs
    path('orders/', OrderListView.as_view(), name='create-list-product'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='products-details'),
]