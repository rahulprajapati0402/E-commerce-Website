from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import get_object_or_404
from django.views import View
from accounts.models import Profile, Cart, CartItem
from products.models import Product, SizeVariant, ColourVariant


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
    colour_variant = request.GET.get('colour')
    size_variant = request.GET.get('size')
    print(size_variant)
    print(colour_variant)
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


def remove_from_cart(request, uid):
    user = request.user
    product = Product.objects.get(uid=uid)
    cart_item = CartItem.objects.filter(cart__user=user, product=product)
    cart_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_page(request):
    user = request.user
    cart_items = CartItem.objects.filter(cart__is_paid=False, cart__user=user)
    cart_total_price = user.carts.first().get_cart_total() if user.carts.first() else 0
    context = {
        "cart_items": cart_items,
        "cart_total_price": cart_total_price
    }
    return render(request, "accounts/cart.html", context)