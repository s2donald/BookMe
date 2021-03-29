from django.contrib import admin
from .models import Product, addOnProducts, GallaryProductImage, MainProductDropDown, ProductDropDown
# Register your models here.

class ProductInline(admin.TabularInline):
    model = addOnProducts
    extra = 0

class GallaryProductInline(admin.TabularInline):
    model = GallaryProductImage
    extra = 0

class MainProductDropDownInline(admin.TabularInline):
    model = MainProductDropDown
    extra = 0

class ProductDropDownInline(admin.TabularInline):
    model = ProductDropDown
    extra = 0


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['business','name', 'request']
    inlines = [ ProductInline, GallaryProductInline, MainProductDropDownInline ]


@admin.register(MainProductDropDown)
class MainProductsDropDownAdmin(admin.ModelAdmin):
    list_display = ['product','placeholder', 'is_required', 'is_multiple']
    inlines = [ ProductDropDownInline ]
