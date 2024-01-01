from django.urls import path
from django.contrib.auth.views import LogoutView
from accounts.views import *


urlpatterns = [
    path("login/", login_page, name="login-url"),
    path("register/", RegisterView.as_view(), name="register-url"),
    path("logout/", LogoutView.as_view(), name="logout-url"),
    path("activate/<email_token>", activate_email, name="activate-account-url"),
    path("cart/", cart_page, name="cart-url"),
    path("add-to-cart/<uid>", add_to_cart, name="add-to-cart-url"),
    path("remove-from-cart/<cart_item_uid>", remove_from_cart, name="remove-from-cart-url"),
    path("remove-coupon/<cart_uid>", remove_coupon, name="remove_coupon"),
    path("success/", payment_success, name="payment_success"),
]