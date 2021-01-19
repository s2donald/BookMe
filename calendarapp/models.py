from django.db import models
from business.models import Company
from consumer.models import Bookings
from businessadmin.models import StaffMember
# Create your models here.

class formBuilder(models.Model):
    booking = models.ForeignKey(Bookings, on_delete=models.CASCADE, related_name='booking_form', null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_booking_form', null=True)

    label = models.CharField(max_length=50, db_index=True)
    checkbox = models.BooleanField(null=True, default=False)
    text = models.TextField(max_length=100, null=True)
    order = models.PositiveIntegerField(default=1)
    is_integer = models.BooleanField(default=False)
    integer = models.IntegerField(null=True)
    is_required = models.BooleanField(default=False)



