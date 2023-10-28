from django.contrib import admin
from accounts.models import Profile, Cart, CartItem

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_paid']

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'size_variant', 'colour_variant']

admin.site.register(Profile)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)