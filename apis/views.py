import json
import redis
from .models import User, Product, Order, OrderItem
from .serializers import UserSerializer, ProductSerializer, OrderSerializer, OrderItemSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

redis_conn = redis.StrictRedis(host='127.0.0.1', port=6379, db=1)
# PRODUCT 
class Product_list(APIView):
    permission_classes = [IsAuthenticated]
    
    '''def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)'''
    
    def get(self, request):
    # Attempt to retrieve data from Redis cache
        cached_data = redis_conn.get('products_list')
        if cached_data:
            cached_data = json.loads(cached_data.decode('utf-8'))
            return Response(cached_data, status=status.HTTP_200_OK)

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        # Serialize the data to JSON and cache it in Redis
        serialized_data = json.dumps(serializer.data)
        redis_conn.set('products_list', serialized_data, ex=3600)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class Product_detail(APIView):
    permission_classes = [IsAuthenticated]
    '''def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'Error': ' Product Does not exist'}, status=status.HTTP_204_NO_CONTENT)'''
        

    def get(self, request, pk):
        # Attempt to retrieve data from Redis cache
        cached_data = redis_conn.get(f'product:{pk}')
        if cached_data:
            cached_data = json.loads(cached_data.decode('utf-8'))
            return Response(cached_data, status=status.HTTP_200_OK)

        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)

            # Serialize the data to JSON and cache it in Redis
            serialized_data = json.dumps(serializer.data)
            redis_conn.set(f'product:{pk}', serialized_data, ex=3600)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'Error': 'Product does not exist'}, status=status.HTTP_204_NO_CONTENT)
                
    def put(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response({'Product Delete': 'Successful'}, status=status.HTTP_204_NO_CONTENT)
    

# USER
class Create_user(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Registration Successful"
            data['username'] = account.username
            data['email'] = account.email
            token = Token.objects.get(user=account).key
            data['token'] = token
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data)


# ORDER
class OrderList(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        order_serializer = OrderSerializer(data=request.data)
        if order_serializer.is_valid():
            order_serializer.save(user=request.user)
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class OrderDetail(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_order(self, pk):
        try:
            return Order.objects.get(pk=pk, user=self.request.user)
        except Order.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        order = self.get_order(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk):
        order = self.get_order(pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        order = self.get_order(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
