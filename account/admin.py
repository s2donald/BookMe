from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
from business.models import Clients, Company, Services
from businessadmin.models import Breaks, StaffMember
from consumer.models import Bookings
from django.contrib.auth.models import Group
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email','date_joined','last_login','is_admin','is_staff', 'is_business', 'is_consumer', 'on_board')
    search_fields = ('email',)
    readonly_fields = ('date_joined','last_login')

    ordering = ('email',)
    filter_horizontal = ()
    list_filter =()
    fieldsets = (
        (None, {'fields': ('email', )}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'phone', 'tz')}),
        (('Permissions'), {'fields': ('is_admin','is_staff', 'is_business', 'is_consumer', 'on_board')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',),
        }),
    )

admin.site.register(Account, AccountAdmin)

class BookingInlines(admin.TabularInline):
    model = Bookings
    extra = 0

class UsersInlines(admin.TabularInline):
    model = Account
    extra = 0

class ServiceInlines(admin.TabularInline):
    model = Services
    extra = 0

class BreaksInline(admin.TabularInline):
    model = Breaks
    extra = 0

@admin.register(Clients)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['user','first_name','last_name','email', 'phone', 'company']
    search_fields = ('user__first_name','email', 'first_name','company__business_name',)
    inlines = [ BookingInlines ]
    
@admin.register(StaffMember)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['company', 'user']
    search_fields = ('user__first_name','company__business_name',)
    inlines = [ BreaksInline ]

    