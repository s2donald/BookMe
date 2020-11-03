from django.db import models
from business.models import Company
from consumer.models import Bookings
# Create your models here.

class formBuilder(models.Model):
    booking = models.ForeignKey(Bookings, on_delete=models.CASCADE, related_name='form')
    label = models.CharField(max_length=50, db_index=True)
    checkbox = models.BooleanField(null=True, default=False)
    text = models.TextField(max_length=100, null=True)
    order = models.PositiveIntegerField(default=1)
    is_required = models.BooleanField(null=True, default=False)



