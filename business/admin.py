from django.contrib import admin
from .models import Company, Category, Services, SubCategory, Amenities, OpeningHours, Gallary
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category']
    prepopulated_fields = {'slug':('name',)}

@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'price_type', 'duration_hour', 'duration_minute']
    prepopulated_fields = {'slug':('name',)}

class GallaryInline(admin.TabularInline):
    model = Gallary

class OpeningHoursInline(admin.TabularInline):
    model = OpeningHours
    extra = 0

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['user','business_name','slug','available','created','updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['available']
    inlines = [ GallaryInline, OpeningHoursInline]

@admin.register(Amenities)
class AmenitiesAdmin(admin.ModelAdmin):
    list_display = ['company','amenity']
