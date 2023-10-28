import uuid
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from base.models import BaseModel
from django.contrib.auth.models import User
from base.emails import send_account_activation_email
from products.models import Product, ColourVariant, SizeVariant


# Create your models here.

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to="profile")

    def __str__(self):
        return self.user.email

    def get_cart_count(self):
        return CartItem.objects.filter(cart__is_paid=False, cart__user=self.user).count()


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price = []
        for cart_item in cart_items:
            price.append(cart_item.product.price)
            if cart_item.colour_variant:
                price.append(cart_item.colour_variant.price)
            if cart_item.size_variant:
                price.append(cart_item.size_variant.price)
        return sum(price)


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    colour_variant = models.ForeignKey(ColourVariant, on_delete=models.SET_NULL, null=True, blank=True)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True, blank=True)

    def get_product_price(self):
        price = [self.product.price]
        if self.size_variant:
            price.append(self.size_variant.price)
        if self.colour_variant:
            price.append(self.colour_variant.price)
        return sum(price)


@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user=instance, email_token=email_token)
            email = instance.email
            send_account_activation_email(email, email_token)
    except Exception as e:
        print(e)