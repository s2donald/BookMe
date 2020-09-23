from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Guest
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
        (('Personal info'), {'fields': ('first_name', 'last_name', 'phone')}),
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

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','email', 'phone', 'address','postal','province','city']