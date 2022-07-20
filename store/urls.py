from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

from .views import SignUpView

urlpatterns = [
    path("", views.home, name="home"),
    path("store/", views.store, name="store"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("about/", views.about, name="about"),
    path("shop/", views.shop, name="shop"),
    path("contact/", views.contact, name="contact"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("update_item/", views.updateItem, name="update_item"),
    path("process_order/", views.process_order, name="process_order"),
    path("productdetail/<int:pk>", views.productdetails, name="productdetails"),


   



]
