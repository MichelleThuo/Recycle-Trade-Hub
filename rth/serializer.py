

from rest_framework import serializers 
from .models import Products,Order

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields=['id','productName', 'photo', 'description', 'price','qty']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        depth=1
        fields=['buyer', 'checkout_request_id', 'products','qty', 'price', 'date','order_status']

