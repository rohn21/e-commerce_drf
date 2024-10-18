from django.contrib import admin
from products_app.models import Product, Customer, Order, OrderItem

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(OrderItem)