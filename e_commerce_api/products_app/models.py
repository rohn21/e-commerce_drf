from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    order_number = models.CharField(max_length=10, unique=True, default='')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    address = models.CharField(max_length=200)
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f'ORD{self.id:05d}'
        super(Order, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.order_number
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.order.order_number} - {self.product.name} ({self.quantity})"