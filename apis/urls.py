from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import Create_user, Product_list, Product_detail, OrderList, OrderDetail


urlpatterns = [
    path('register/', Create_user.as_view(), name='register-user' ),
    path('login/', obtain_auth_token, name='login-user'),
    path('products/', Product_list.as_view(), name='product-list'),
    path('products/<int:pk>', Product_detail.as_view(), name='product-detail'),
    path('orders/', OrderList.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetail.as_view(), name='order-detail'),
]