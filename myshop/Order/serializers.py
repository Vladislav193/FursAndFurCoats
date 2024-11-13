from rest_framework import serializers
from .models import Order, OrderItem
from Category.serializers import ProductSerializers


class OrderItemSerializers(serializers.ModelSerializer):
    product = ProductSerializers()
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializers(serializers.ModelSerializer):
    items = OrderItemSerializers(source='orderitem_set', many=True)
    class Meta:
        model = Order
        fields = ['user', 'price', 'created_at', 'items']