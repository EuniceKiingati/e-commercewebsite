from django.shortcuts import render
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import JsonResponse
import json


# Create your views here.
def home(request):
    context={}
    return render(request, 'store/home.html', context)

def store(request):
    products=Product.objects.all()
    context={'products':products}
    return render(request, 'store/store.html', context)

def shop(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created=Order.objects.get_or_create(customer=customer)
        items=order.orderitem_set.all()
        cartItems= order.get_cart_item
    else:
        items=[]
        order={'get_cart_total':0, 'get_cart_item':0}
        cartItems= order['get_cart_item']

    products=Product.objects.all()
    context={'products':products,'cartItems':cartItems }
    return render(request, 'store/shop.html', context)
    
def about(request):
    context={}
    return render(request, 'store/about.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created=Order.objects.get_or_create(customer=customer, complete=False)
        items=order.orderitem_set.all()
        cartItems= order.get_cart_item
    else:
        items=[]
        order={'get_cart_total':0, 'get_cart_item':0}
        cartItems=order['get_cart_item','order':order]
    context={'items':items, 'order':order, 'cartItems':cartItems}
    # 'order':order

    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created=Order.objects.get_or_create(customer=customer, complete=False)
        items=order.orderitem_set.all()
        cartItems= order.get_cart_item

    else:
        items=[]
        order={'get_cart_total':0, 'get_cart_item':0}
        cartItems= order.get_cart_item

    context={'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)
    
def contact(request):
    context={}
    return render(request, 'store/contact.html', context)

#def signup(request):
    #context={}
    #return render(request, 'store/signup.html', context)

def login(request):
    context={}
    return render(request, 'store/login.html', context)


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def updateItem(request):

    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    print('action:', action)
    print('productId:',productId )

    customer=request.user.customer
    product=Product.objects.get(id=productId)
    order, created=Order.objects.get_or_create(customer=customer,complete=False)
    orderItem, created=OrderItem.objects.get_or_create(order=order,product=product)
    
    if action=='add':
        orderItem.quantity=(orderItem.quantity + 1)
    elif action=='remove' :
        orderItem.quantity=(orderItem.quantity - 1)
  
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
    
    
    
    return JsonResponse('Item was added', safe=False)


