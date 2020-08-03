from django.db import models
from business.models import Account, Company
# Create your models here.

class Bookings(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    #We must add a timeslot for the booking
    has_paid = models.BooleanField(default=False)
    #We must also create a receipt model to handle the reciepts and link to the booking


