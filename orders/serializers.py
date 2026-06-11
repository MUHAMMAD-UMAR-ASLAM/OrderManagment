from django.db import  transaction
from rest_framework import serializers

from orders.models import Order, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


