from rest_framework import serializers
import bleach
from django.contrib.auth.models import User
from .models import MenuItem,Category,Cart,Order,OrderItem

class MenuItemSerializer(serializers.ModelSerializer):
    def validate_title(self, value):
        return bleach.clean(value)
    
    def validate_price(self, value):
        if (value < 2):
            raise serializers.ValidationError('Price should not be less than 2.0')

    def validate_inventory(self, value):
        if value is None:
            raise serializers.ValidationError("Inventory is required.")
        if value < 0:
            raise serializers.ValidationError("Inventory cannot be negative.")
        return value
        
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value

    class Meta:
        model =MenuItem
        fields = ['id' ,'title', 'price','inventory','category']
        extra_kwargs = {
            'price': {'required': True},
            'inventory': {'required': True}
        }


class CartSerializer(serializers.ModelSerializer):
    def validate_quantity(self, value):
        if value is 1:
            return serializers.ValidationError("Invalid Value ")


    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity','unit_price','price']



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model =Order
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email'] 
       