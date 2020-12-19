from django.contrib import admin
from businessadmin.models import StaffMember
from .models import Company, Category, Services, SubCategory, Amenities, OpeningHours, Gallary, Clients, CompanyReq, ServiceCategories
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
    list_display = ['business','name', 'slug', 'price', 'price_type', 'duration_hour', 'duration_minute']
    prepopulated_fields = {'slug':('name',)}

class GallaryInline(admin.TabularInline):
    model = Gallary
    extra = 0

class OpeningHoursInline(admin.TabularInline):
    model = OpeningHours
    extra = 0

class AmenitiesInline(admin.TabularInline):
    model = Amenities
    extra = 0

class ClientsInline(admin.TabularInline):
    model = Clients
    extra = 0

class CompanyReqInline(admin.TabularInline):
    model = CompanyReq
    extra = 0

class ServiceCategories(admin.TabularInline):
    model = ServiceCategories
    extra = 0

class StaffMemberInline(admin.TabularInline):
    model = StaffMember
    extra = 0

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['user','business_name','slug','available','created','updated']
    exclude = ['location']
    list_filter = ['available', 'created', 'updated']
    search_fields = ('user__first_name','business_name','user__email')
    list_editable = ['available']
    inlines = [ StaffMemberInline, ClientsInline, CompanyReqInline, GallaryInline, OpeningHoursInline, AmenitiesInline, ServiceCategories ]




