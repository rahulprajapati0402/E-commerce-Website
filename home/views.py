from django.shortcuts import render
from django.views import View
from products.models import Product, Category

# Create your views here.


def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        "products": products,
        "categories": categories
    }
    return render(request, "home/index.html", context)


class IndexView(View):
    template_name = "home/index.html"

    def get(self, request):
        products = Product.objects.all()
        categories = Category.objects.all()
        context = {
            "products": products,
            "categories": categories
        }
        return render(request, self.template_name, context)