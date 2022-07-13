from django.shortcuts import render
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


# Create your views here.
def home(request):
    context={}
    return render(request, 'store/home.html', context)

def store(request):
    products=Product.objects.all()
    context={'products':products}
    return render(request, 'store/store.html', context)

def shop(request):
    products=Product.objects.all()
    context={'products':products}
    return render(request, 'store/shop.html', context)
    
def about(request):
    context={}
    return render(request, 'store/about.html', context)

def cart(request):
    context={}
    return render(request, 'store/cart.html', context)

def checkout(request):
    context={}
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