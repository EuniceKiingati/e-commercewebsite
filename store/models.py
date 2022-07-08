from audioop import maxpp
from re import T
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

 

class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name=models.CharField(max_length=255, null=True)
    last_name=models.CharField(max_length=255)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=255)
    birth_date=models.DateField(null=True)
    
    def __str__(self):
        return self.name 

class Product(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField()
    unit_price=models.DecimalField(max_digits=10, decimal_places=2)
    digital=models.BooleanField(default=False, null=True, blank=False)
    image=models.ImageField(null=True, blank=True)
    
    @property# to avoid crashing when one product doesnt have an image
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url


    def __str__(self):
        return self.name 



class Order(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.PROTECT, null=True, blank=True)
    date_ordered=models.DateTimeField(auto_now=True)
    complete=models.BooleanField(default=False)
    transaction_id=models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name 


class OrderItem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.PROTECT, null=True)
    product=models.ForeignKey(Product, on_delete=models.PROTECT, null=True)
    quantity=models.PositiveSmallIntegerField(default=0,null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    order=models.ForeignKey(Order, on_delete=models.PROTECT, null=True)
    address=models.CharField(max_length=255, null=False)
    city=models.CharField(max_length=255, null=False)
    area=models.CharField(max_length=255, null=False)
    building=models.CharField(max_length=255, null=False)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name 