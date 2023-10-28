from django.db import models
from django.utils.text import slugify
from base.models import BaseModel


class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_image = models.ImageField(upload_to="categories")

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.category_name


class ColourVariant(BaseModel):
    colur_name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.colur_name


class SizeVariant(BaseModel):
    size_name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.size_name


class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    price = models.IntegerField()
    product_description = models.TextField()
    colour = models.ManyToManyField(ColourVariant, blank=True)
    size = models.ManyToManyField(SizeVariant, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.product_name

    def get_product_price_by_size(self, size):
        return self.price + SizeVariant.objects.get(size_name=size).price

    def get_product_price_by_colour(self, colour):
        return self.price + ColourVariant.objects.get(colur_name=colour).price

    def get_image_by_colour(self, colour):
        colour = ColourVariant.objects.get(colur_name=colour)
        return ProductImage.objects.filter(product=self.uid, colour=colour.uid).first().image


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    colour = models.ForeignKey(ColourVariant, on_delete=models.CASCADE, related_name="image_colour")
    image = models.ImageField(upload_to="product")


class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount = models.IntegerField(default=100)
    min_price = models.IntegerField(default=500)

    def __str__(self):
        return self.coupon_code
