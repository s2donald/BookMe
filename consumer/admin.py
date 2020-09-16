from django.contrib import admin
from .models import Bookings, Reviews
# Register your models here.

@admin.register(Bookings)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['company','service','user', 'start', 'end', 'price', 'price_paid']

@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer','company','review', 'star', 'created']