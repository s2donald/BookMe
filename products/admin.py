from django.contrib import admin
from .models import Product, addOnProducts, GallaryProductImage
# Register your models here.

class ProductInline(admin.TabularInline):
    model = addOnProducts
    extra = 0

class GallaryProductInline(admin.TabularInline):
    model = GallaryProductImage
    extra = 0

@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name','description', 'slug', 'price', 'stock', 'request', 'mainimage']
    inlines = [ ProductInline, GallaryProductInline ]