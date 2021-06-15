from django.contrib import admin
from .models import CompanyShippingZone, PriceBasedShippingRate, Post, Comment
from .forms import ShippingZoneForm

# Register your models here.

@admin.register(CompanyShippingZone)
class ShippingZoneAdmin(admin.ModelAdmin):
    list_display = ['name']
    form = ShippingZoneForm

@admin.register(PriceBasedShippingRate)
class PriceBasedShippingAdmin(admin.ModelAdmin):
    list_display = ['names','company', 'rate']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')