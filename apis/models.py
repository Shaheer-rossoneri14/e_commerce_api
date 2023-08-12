from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
from django.utils.timezone import now

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        
# Create your models here.

# User Model
class User(AbstractUser):
    id = models.AutoField(primary_key=True) #Auto-incrementing unique identifier
    username = models.CharField(max_length=50, unique=True) #Unique username
    password = models.CharField(max_length=128) #Hashed password
    email = models.EmailField(unique=True)  #Unique email
    date_joined = models.DateTimeField(auto_now_add=True)   #Date and time the user joined

    def __str__(self):
        return self.username
    
# Product Model    
class Product(models.Model):
    id = models.AutoField(primary_key=True) #Auto-incrementing unique identifier
    name = models.CharField(max_length=255) #Name of the product
    description = models.CharField(max_length=500)    #Description of the product
    price = models.DecimalField(max_length=15, max_digits=10, decimal_places=2)    #Price of the product
    date_created = models.DateTimeField(auto_now_add=True)  #Date and time the product was added  
    date_updated = models.DateTimeField(auto_now=True)  #Date and time product was last updated

    def __str__(self):
        return self.name
    
# Order Model
class Order(models.Model):
    id = models.AutoField(primary_key=True) #Auto-incrementing unique identifier
    user = models.ForeignKey(User, on_delete=models.CASCADE)    #Foreign Key linking to the User that placed order
    date_placed = models.DateTimeField(default=now)    #Date and time the order was placed
    status_choices = [  
        ('placed', 'Placed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=status_choices)    #Current status of the order

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    
# Order Item Model    
class OrderItem(models.Model):
    id = models.AutoField(primary_key=True) #Auto-incrementing unique identifier
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  #Foreign Key linking to the Order
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  #Foreign Key linking to the Product 
    quantity = models.PositiveIntegerField()    #Number of that product in the order

    def __str__(self):
        return f"Item {self.id} in Order #{self.order.id}"