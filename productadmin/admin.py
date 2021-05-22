from django.contrib import admin
from .models import CompanyShippingZone, PriceBasedShippingRate
from .forms import ShippingZoneForm

# Register your models here.

@admin.register(CompanyShippingZone)
class ShippingZoneAdmin(admin.ModelAdmin):
    list_display = ['name']
    form = ShippingZoneForm

@admin.register(PriceBasedShippingRate)
class PriceBasedShippingAdmin(admin.ModelAdmin):
    list_display = ['name','company', 'rate']
    