from django.db import models
from business.models import Account, Company, Services
from django.utils import timezone
# Create your models here.

class Bookings(models.Model):
    #The user who booked
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    #The company that was booked
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    #The service booked
    service = models.OneToOneField(Services, on_delete=models.CASCADE)
    #We must add a timeslot for the booking
    has_paid = models.BooleanField(default=False)
    #We must also create a receipt model to handle the reciepts and link to the booking
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)

    #is the service available at this time
    is_avail = models.BooleanField(default=False)
    class Meta:
        ordering = ('service',)
        verbose_name = 'booking'
        verbose_name_plural = 'bookings'



