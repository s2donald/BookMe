from django.db import models
from business.models import Company, Clients, CompanyReq
from gibele.utils import unique_slug_generator_product, unique_slug_generator_order
from django.db.models.signals import pre_save
from django.utils import timezone
from account.models import Account
from django.core.validators import MinValueValidator, MaxValueValidator,RegexValidator
from address.models import AddressField
from django_countries.fields import CountryField
from cities.models import City, Region
from decimal import Decimal

# Create your models here.
shiptype = (
    ('fixed', "Fixed"),
)
class PriceBasedShippingRate(models.Model):
    names=models.CharField(verbose_name='', max_length=200)
    company = models.ForeignKey(Company, related_name='shipping_pricebased', on_delete=models.CASCADE, blank=True, null=True)
    lower_price = models.DecimalField(verbose_name='Minimum Order Price', decimal_places=2, default=Decimal('0.00'), max_digits=12, validators=[MinValueValidator(Decimal('0.00'))])
    upper_price = models.DecimalField(verbose_name='Maximum Order Price', decimal_places=2, max_digits=12, blank=True, null=True, validators=[MinValueValidator(Decimal('0.01'))])
    rate = models.DecimalField(verbose_name='Rate Amount', decimal_places=2, max_digits=12, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
    # def clean(self):
    #     cleaned_data = super().clean()
    #     st = cleaned_data['lower_price']
    #     end = cleaned_data['upper_price']
    #     if st > end :
    #          raise forms.ValidationError('The minumum order price can not be larger than the maximum order price.')
    #     return cleaned_data
    def __str__(self):
        return f'{self.names} - {self.company.business_name}'
    class Meta:
        ordering = ('company',)
        unique_together = ['company','names']
        verbose_name = 'Price Based Shipping Rate'
        verbose_name_plural = 'Price Based Shipping Rates'

class CompanyShippingZone(models.Model):
    company = models.ForeignKey(Company, related_name='shipping_zones_avail', on_delete=models.CASCADE, blank=True, null=True)
    pricebased_rate = models.ManyToManyField(PriceBasedShippingRate, blank=True, related_name='pricebased_rates')
    name = models.CharField(max_length=200, verbose_name='')
    country = CountryField(multiple=True, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    city = models.ManyToManyField(City, verbose_name='City', blank=True)
    state = models.ManyToManyField(Region, verbose_name='State or Province', blank=True)
    def __str__(self):
        return f'{self.name}'
    class Meta:
        ordering = ('company',)
        verbose_name = 'Shipping Zone'
        verbose_name_plural = 'Shipping Zone'

# class Shipping(models.Model):
#     pricebased_rate = models.ForeignKey(PriceBasedShippingRate, blank=True, null=True, related_name='pricebased_rates', on_delete=models.CASCADE)
#     shipping_zone = models.ForeignKey(ShippingZone, blank=True, null=True, related_name='shipping_zones', on_delete=models.CASCADE)
#     class Meta:
#         verbose_name = 'Shipping'
#         verbose_name_plural = 'Shipping'
#     def __str__(self):
#         return f'{self.shipping_zone}'