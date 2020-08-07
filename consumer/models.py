from django.db import models
from business.models import Account, Company, Services
from django.utils import timezone

# Create your models here.

class Bookings(models.Model):
    #The user who booked
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    #The service booked (also contains the company the service is with)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    #The company which is offering this service
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    #We must add a timeslot for the booking
    #Has the booking been paid for
    has_paid = models.BooleanField(default=False)
    #We must also create a receipt model to handle the reciepts and link to the booking
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)
    #is the service available at this time
    is_avail = models.BooleanField(default=False)
    class Meta:
        ordering = ('start',)
        verbose_name = 'booking'
        verbose_name_plural = 'bookings'

    def __str__(self):
        return self.service.name



