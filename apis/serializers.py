from rest_framework import serializers
from .models import User, Product, Order, OrderItem
from drf_writable_nested import WritableNestedModelSerializer 

# User
class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type' : 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'date_joined']
        extra_kwargs = {
            'password' : {'write_only' : True}
        }
    
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password!=password2:
            raise serializers.ValidationError({'error': 'Password and Password2 should be same'})
        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()

        return account

        
# Product
class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = "__all__"


# Orders
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        

class OrderSerializer(WritableNestedModelSerializer,
                        serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        order_items_data = validated_data.pop('orderitem_set')
        order = Order.objects.create(**validated_data)
        
        for order_item_data in order_items_data:
            OrderItem.objects.create(order=order, **order_item_data)
            
        return order