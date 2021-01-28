from django.contrib import admin
from .models import formBuilder, bookingForm
# Register your models here.

@admin.register(formBuilder)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['company', 'label']