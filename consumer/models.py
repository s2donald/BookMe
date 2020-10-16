from django.db import models
from business.models import Account, Company, Services, Clients
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator,RegexValidator
from django.db.models.signals import pre_save
from gibele.utils import unique_slug_generator_booking
from django.core.exceptions import ValidationError
# Create your models here.

class Bookings(models.Model):
    #The user's information name who booked
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    guest = models.ForeignKey(Clients, on_delete=models.CASCADE, null=True, blank=True)
    # first_name = models.CharField(verbose_name="First Name", max_length=30, unique=False,null=True, blank=True)
    # last_name = models.CharField(verbose_name="Last Name", max_length=30, unique=False, null=True, blank=True)
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # phone = models.CharField(verbose_name="Phone Number",validators=[phone_regex], max_length=17, null=True, blank=True)
    # address = models.CharField(max_length=200, null=True, blank=True)
    # postal = models.CharField(max_length=35, null=True, blank=True)
    # province = models.CharField(max_length=35, null=True, blank=True)
    # city = models.CharField(max_length=35, null=True, blank=True)
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
    is_cancelled = models.BooleanField(default=False)
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
    reviewer = models.ForeignKey(Account, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_reviews')
    review = models.TextField(max_length=200)
    star = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('star',)
        unique_together=(('reviewer','company'),)
        index_together=(('reviewer','company'),)
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'




