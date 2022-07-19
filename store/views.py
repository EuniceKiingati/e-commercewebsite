from django.shortcuts import render
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import JsonResponse
import json
import datetime


def get_user_cart_item_count(request):
    if request.user.is_authenticated:
        order =  Order.objects.filter(
            customer__user=request.user, complete=False).first()
        if order:
            return order.get_cart_item
    return 0

# Create your views here.


def home(request):
    products = Product.objects.all()[:3]
    products2 = Product.objects.all()[3:6]
    cart_item_count =get_user_cart_item_count(request)

    context = {"products": products, "products2": products2,
               'cart_item_count': cart_item_count}
    return render(request, "store/home.html", context)


def store(request):
    products = Product.objects.all()
    cart_item_count =get_user_cart_item_count(request)
    context = {"products": products, 'cart_item_count':cart_item_count}
    return render(request, "store/store.html", context)


def shop(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_item_count = order.get_cart_item
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_item": 0, "shipping": False}
        cart_item_count = order["get_cart_item"]

    products = Product.objects.all()
    products3 = Product.objects.all()[2:4]
    context = {"products": products,
               "cart_item_count": cart_item_count, "products3": products3, }
    return render(request, "store/shop.html", context)


def about(request):
    cart_item_count =get_user_cart_item_count(request)
    context = {'cart_item_count':cart_item_count}
    return render(request, "store/about.html", context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_item": 0, "shipping": False}
        cartItems = order["get_cart_item", "order":order]
    context = {"items": items, "order": order, "cartItems": cartItems}
    # 'order':order

    return render(request, "store/cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item

    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_item": 0, "shipping": False}
        cartItems = order.get_cart_item

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/checkout.html", context)


def contact(request):
    cart_item_count =get_user_cart_item_count(request)
    context = {'cart_item_count':cart_item_count}
    return render(request, "store/contact.html", context)


# def signup(request):
# context={}
# return render(request, 'store/signup.html', context)


def login(request):
    context = {}
    return render(request, "store/login.html", context)


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def updateItem(request):

    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    print("action:", action)
    print("productId:", productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == "add":
        orderItem.quantity = orderItem.quantity + 1

    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        orderitems = order.orderitem_set.all()
        for orderitem in orderitems:
            product = orderitem.product
            product.in_stock -= orderitem.quantity
            product.save()
            breakpoint()
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                area=data['shipping']['area'],
                building=data['shipping']['building'],



            )

    else:
        print("user not logged in")
    return JsonResponse('Payment complete', safe=False)
