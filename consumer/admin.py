from django.contrib import admin
from .models import Bookings
# Register your models here.

@admin.register(Bookings)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['service','user', 'company', 'start', 'end', 'has_paid']