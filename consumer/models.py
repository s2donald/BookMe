from django.db import models
from business.models import Account, Company, Services, Clients
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator,RegexValidator
from django.db.models.signals import pre_save
from gibele.utils import unique_slug_generator_booking
from django.core.exceptions import ValidationError
# Create your models here.
hours_choices = (
    (0,'0 Hours'),
    (1, '1 Hour'),
    (2, '2 Hours'),
    (3, '3 Hours'),
    (4, '4 Hours'),
    (5, '5 Hours'),
    (6, '6 Hours'),
    (7, '7 Hours'),
    (8, '8 Hours'),
    (9, '9 Hours'),
    (10, '10 Hours'),
    (11, '11 Hours'),
    (12, '12 Hours'),
    (13, '13 Hours'),
    (14, '14 Hours'),
    (15, '15 Hours'),
    (16, '16 Hours'),
    (17, '17 Hours'),
    (18, '18 Hours'),
    (19, '19 Hours'),
    (20, '20 Hours'),
    (21, '21 Hours'),
    (22, '22 Hours'),
    (23, '23 Hours')
 )

minute_choices = (
    (0, '0 Minutes'),
    (5, '5 Minutes'),
    (10, '10 Minutes'),
    (15, '15 Minutes'),
    (20, '20 Minutes'),
    (25, '25 Minutes'),
    (30, '30 Minutes'),
    (35, '35 Minutes'),
    (40, '40 Minutes'),
    (45, '45 Minutes'),
    (50, '50 Minutes'),
    (55, '55 Minutes')
 )

class Bookings(models.Model):
    #The user's information name who booked
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    guest = models.ForeignKey(Clients, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(max_length=200, db_index=True, blank=True, unique=True)
    #The service booked (also contains the company the service is with)
    service = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='bookings', related_query_name="bookings")
    #The company which is offering this service
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    #We must add a timeslot for the booking
    #The amount the booking has been paid for
    price_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    #The price of the booking
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    #company cancelled booking
    is_cancelled_company = models.BooleanField(default=False)
    #user cancelled booking
    is_cancelled_user = models.BooleanField(default=False)
    #We must also create a receipt model to handle the reciepts and link to the booking
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ('start',)
        verbose_name = 'booking'
        verbose_name_plural = 'bookings'

    def __str__(self):
        return self.service.name
    def clean(self):
        super().clean()
        if self.user is None and self.guest is None:
            raise ValidationError('You must add a client to the booking!')

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_booking(instance)

pre_save.connect(slug_generator, sender=Bookings)

class Reviews(models.Model):
    reviewer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='user_reviews')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_reviews')
    review = models.TextField(max_length=500)
    star = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('star',)
        unique_together=(('reviewer','company'),)
        index_together=(('reviewer','company'),)
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

def get_booking_folder(instance, filename):
    return "booking/extrainfo/".format(instance.booking.id, filename)

class extraInformation(models.Model):
    booking = models.OneToOneField(Bookings, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, blank=True, null=True)
    photo = models.ImageField(upload_to=get_booking_folder, blank=True, null=True)
    #For car services only
    car_make = models.CharField(max_length=30, blank=True, null=True)
    car_model = models.CharField(max_length=30, blank=True, null=True)
    car_year = models.IntegerField(blank=True, null=True)


    





