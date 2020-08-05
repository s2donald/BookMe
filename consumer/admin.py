from django.contrib import admin
from .models import Bookings
# Register your models here.

@admin.register(Bookings)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['company','service','user', 'start', 'end', 'has_paid']