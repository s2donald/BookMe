from django.contrib import admin
from .models import Product, GallaryProductImage, MainProductDropDown, ProductDropDown, ProductReviews, Order, OrderItem, ProductCategory, OrderItem, QuestionModels, AnswerModels
from django_hosts.resolvers import reverse
from django.utils.safestring import mark_safe
# Register your models here.

class GallaryProductInline(admin.TabularInline):
    model = GallaryProductImage
    extra = 0

class MainProductDropDownInline(admin.TabularInline):
    model = MainProductDropDown
    extra = 0

class ProductDropDownInline(admin.TabularInline):
    model = ProductDropDown
    extra = 0

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'company']
    prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['business','name', 'request']
    inlines = [ GallaryProductInline, MainProductDropDownInline ]

@admin.register(QuestionModels)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['question','product']

@admin.register(AnswerModels)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['question','orderitem']

@admin.register(MainProductDropDown)
class MainProductsDropDownAdmin(admin.ModelAdmin):
    list_display = ['product','placeholder', 'is_required', 'is_multiple']
    inlines = [ ProductDropDownInline ]

@admin.register(ProductReviews)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['reviewer','guest', 'product']

def order_pdf(obj):
    url = reverse('admin_order_pdf', args=(obj.id,), host='prodadmin')
    return mark_safe(f'<a href="{url}">PDF</a>')

order_pdf.short_description = 'Invoice'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'company','slug', 'first_name', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [ OrderItemInline ]

