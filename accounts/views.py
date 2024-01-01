import razorpay
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from accounts.models import Profile, Cart, CartItem
from products.models import Product, SizeVariant, ColourVariant, Coupon


def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=email)
        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)

        user = authenticate(username=email, password=password)
        if user:
            try:
                user_profile = get_object_or_404(Profile, user=user_obj.first())
            except Exception as e:
                return HttpResponse('Kindly contact our customer support team.')
            if not user_profile.is_email_verified:
                messages.warning(request, 'Your account is not verified.')
                return HttpResponseRedirect(request.path_info)
            login(request, user)
            return redirect('/')
        messages.warning(request, 'Invalid credentials !!')
        return HttpResponseRedirect(request.path_info)
    return render(request, 'accounts/login.html')


class RegisterView(View):
    template_name = 'accounts/register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username=email)
        if user.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)

        user = User.objects.create(first_name=first_name, last_name=last_name, email=email, username=email)
        user.set_password(password)
        user.save()
        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)


def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username=email)
        if user.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)

        user = User.objects.create(first_name=first_name, last_name=last_name, email=email, username=email)
        user.set_password(password)
        user.save()
        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)
    return render(request, 'accounts/register.html')


def activate_email(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse("Invalid Email Token")


def add_to_cart(request, uid):
    user = request.user
    if user.is_authenticated:
        colour_variant = request.GET.get('colour')
        size_variant = request.GET.get('size')
        product = Product.objects.get(uid=uid)
        cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
        cart_item = CartItem.objects.create(cart=cart, product=product)
        if size_variant:
            variant = SizeVariant.objects.get(size_name=size_variant)
            cart_item.size_variant = variant
            cart_item.save()
        if colour_variant:
            variant = ColourVariant.objects.get(colur_name=colour_variant)
            cart_item.colour_variant = variant
            cart_item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('login-url')


def remove_from_cart(request, cart_item_uid):
    user = request.user
    if user.is_authenticated:
        cart_item = CartItem.objects.filter(cart__user=user, uid=cart_item_uid)
        cart_item.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('login-url')


def cart_page(request):
    user = request.user
    if user.is_authenticated:
        cart = None
        try:
            cart = Cart.objects.get(user=user, is_paid=False)
        except Exception as e:
            print(e)
        if request.method == "POST":
            coupon = request.POST.get("coupon")
            coupon_obj = Coupon.objects.filter(coupon_code=coupon).first()
            if not coupon_obj:
                messages.warning(request, "Coupon not found.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if not cart.get_cart_total() > coupon_obj.min_price:
                messages.warning(request, f"Minimum amount to apply coupon is {coupon_obj.min_price}.")
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            if cart.coupon == coupon_obj:
                messages.warning(request, "Coupon already applied.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if coupon_obj:
                cart.coupon = coupon_obj
                cart.save()
                messages.success(request, "Coupon added successfully.")
        payment = None
        razorpay_key_id = settings.RAZORPAY_KEY_ID
        if cart:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
            payment = client.order.create({"amount": cart.get_cart_total() * 100, "currency": "INR", "payment_capture": 1})
        context = {"cart": cart, "payment": payment, "razorpay_key_id": razorpay_key_id}
        return render(request, "accounts/cart.html", context)
    return redirect('login-url')


def remove_coupon(request, cart_uid):
    cart = Cart.objects.get(uid=cart_uid)
    cart.coupon = None
    cart.save()
    messages.success(request, "Coupon removed successfully.")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def payment_success(request):
    order_id = request.GET.get("order_id")
    cart_obj = Cart.objects.get(razorpay_order_id=order_id)
    cart_obj.is_paid=True
    cart_obj.save()
    return HttpResponse("Payment Success.")
