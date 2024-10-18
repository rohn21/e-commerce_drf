from rest_framework import serializers
from products_app.models import Product, Order, OrderItem, Customer
from datetime import date

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
        
    # validation for unique customer_name
    def validate_name(self, value):
        queryset = Customer.objects.filter(name=value).exists()
        if queryset:
            raise serializers.ValidationError("Customer with this name already exists.")
        return value

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
    
    # validation for unique product_name
    def validate_name(self, value):
        queryset = Product.objects.filter(name=value).exists()
        if queryset:
            raise serializers.ValidationError("Product with this name already exists.")
        return value
    
    # validation for positive and limited weight of product
    def validate_weight(self, value):
        if value <= 0:
            raise serializers.ValidationError("Weight must be positive value.")
        if value > 25:
            raise serializers.ValidationError("Weight cannot more than 25kg.")
        return value

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    
    class Meta: 
        model = OrderItem
        fields = "__all__"
        extra_kwargs = {
            'order': {'required': False}
        }
        
class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    order_items = OrderItemSerializer(many=True, write_only=True)
    order_item_list = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('order_number', 'customer', 'order_date', 'address', 'order_items', 'order_item_list')
        
    # displays list of item in response in POST,GET 
    def get_order_item_list(self, obj):
        order_items = obj.orderitem_set.all()
        return OrderItemSerializer(order_items, many=True).data
    
    # order's total_weight related validation
    def validate(self, attrs):
        order_items = attrs.get('order_items', [])
        if not order_items and self.instance is None:
            raise serializers.ValidationError('Order must have at least one item')
        
        total_weight = sum(item.get('product').weight * item.get('quantity') for item in order_items)
        # print('➡ e_commerce_api/products_app/serializers.py:68 total_weight:', total_weight)
        if total_weight > 150:
            raise serializers.ValidationError("Order cumulative weight must be under 150kg.")
        
        attrs['order_items'] = order_items
        return attrs
    
    # date valiadtion
    def validate_order_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Order date cannot be in past.")
        return value

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items', [])
        order = Order.objects.create(**validated_data)
        if order_items_data:
            for order_item in order_items_data:
                OrderItem.objects.create(order=order, **order_item)
        return order
        
    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('order_items', [])
        instance.customer = validated_data.get('customer', instance.customer)
        instance.address = validated_data.get('address', instance.address)
        instance.save() 
        
        if order_items_data:
            instance.orderitem_set.all().delete()
            for order_item in order_items_data:
                OrderItem.objects.create(order=instance, **order_item)   
                    
        instance.save() 
        return instance