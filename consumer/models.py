from django.db import models
from business.models import Account, Company, Services
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator,RegexValidator

# Create your models here.

class Bookings(models.Model):
    #The user's information name who booked
    guest = Account.objects.get(email='guest@gibele.com')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, default=guest)
    first_name = models.CharField(verbose_name="First Name", max_length=30, unique=False,null=True, blank=True)
    last_name = models.CharField(verbose_name="Last Name", max_length=30, unique=False, null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(verbose_name="Phone Number",validators=[phone_regex], max_length=17, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    postal = models.CharField(max_length=35, null=True, blank=True)
    province = models.CharField(max_length=35, null=True, blank=True)
    city = models.CharField(max_length=35, null=True, blank=True)

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

class Reviews(models.Model):
    reviewer = models.ForeignKey(Account, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    review = models.TextField(max_length=200)
    star = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created',)
        unique_together=(('reviewer','company'),)
        index_together=(('reviewer','company'),)
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'



