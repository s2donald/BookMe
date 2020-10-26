from django.contrib import admin
from .models import Bookings, Reviews, extraInformation
# Register your models here.


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer','company','review', 'star', 'created']

class extraInformationInline(admin.TabularInline):
    model = extraInformation
    extra = 0

@admin.register(Bookings)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['company','service','user', 'start', 'end', 'price', 'price_paid']
    inlines = [extraInformationInline]