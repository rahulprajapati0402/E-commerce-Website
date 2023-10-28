from django.shortcuts import render, redirect
from products.models import Product


def product_page(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        context = {
            "product": product
        }
        if request.GET.get('size'):
            size = request.GET.get('size')
            price = product.get_product_price_by_size(size)
            context["selected_size"] = size
            context["updated_price"] = price

        if request.GET.get('colour'):
            colour = request.GET.get('colour')
            price = product.get_product_price_by_colour(colour)
            image = product.get_image_by_colour(colour)
            context["selected_colour"] = colour
            context["updated_colour_price"] = price
            context["colour_image"] = image
        return render(request, "products/product.html", context)
    except Exception as e:
        print(e)
        return render(request, "base/error.html")
