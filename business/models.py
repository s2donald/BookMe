from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from django.core.validators import RegexValidator
from account.models import Account, MyAccountManager
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.db.models.signals import pre_save
from gibele.utils import unique_slug_generator
# This category holds our different types of services such as
#   automotive services, health and wellness services, home services, etc
#   These should not be modified by the user
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("business:company_list_by_category", args=[self.slug])

class SubCategory(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    class Meta:
        ordering = ('name',)
        verbose_name = 'sub-category'
        verbose_name_plural = 'sub-categories'
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("business:company_list_by_category", args=[self.slug])

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

WEEKDAYS = [
  (0, ("Sunday")),
  (1, ("Monday")),
  (2, ("Tuesday")),
  (3, ("Wednesday")),
  (4, ("Thursday")),
  (5, ("Friday")),
  (6, ("Saturday")),
]

INTERVAL = [
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
]

price_choices = (
    ('fixed','Fixed'),
    ('start','Starting Price'),
    ('variable','Variable'),
    ('dont','Don\'t Show'),
    ('free','Free')
)
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
 
beforeafter = (
    ('none', '-'),
    ('before','Before'),
    ('after','After'),
    ('bf','Before & After')
 )


#This is the model for the information we need from each company that is listed on the website
class Company(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='user')
    business_name = models.CharField(max_length=30, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category', null=True, blank=True)
    subcategory = models.ManyToManyField(SubCategory)
    description = models.TextField(max_length=200, db_index=True, blank=True)
    address = models.CharField(max_length=200)
    avgrating = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    postal_regex = RegexValidator(regex=r"^[ABCEGHJKLMNPRSTVXY]{1}\d{1}[A-Z]{1} *\d{1}[A-Z]{1}\d{1}$", message="A valid postal code/ZIP Code must be entered")
    postal = models.CharField(max_length=10, validators=[postal_regex])
    state = models.CharField(max_length=2)
    city = models.CharField(max_length=30)
    slug = models.SlugField(max_length=200, db_index=True, blank=True, unique=True)
    interval = models.IntegerField(choices=INTERVAL, default=1)
    image = models.ImageField(upload_to='companies/%Y/%m/%d', blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ('-publish',)
        verbose_name = 'company'
        verbose_name_plural = 'companies'
        index_together =(('slug','id'),)
        
    def __str__(self):
        return self.business_name

    def get_account_url(self):
        return reverse('account:company_detailed', args=[self.slug, self.id])

    def get_schedule_url(self):
        return reverse('account:booking_business', args=[self.slug, self.id])

    def get_absolute_url(self):
        return reverse("business:company_detail", args=[self.slug,self.id])

    def get_booking_url(self):
        return reverse("calendarapp:bookingurls", args=[self.slug])



def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Company)

class OpeningHours(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='hours')
    weekday = models.IntegerField(choices=WEEKDAYS)
    from_hour = models.TimeField(default='9:00:00')
    to_hour = models.TimeField(default='17:00:00')
    is_closed = models.BooleanField(default=False)
    class Meta:
        ordering = ('weekday', 'from_hour')
        unique_together = ('weekday', 'company')

    def __unicode__(self):
        return u'%s: %s - %s' % (self.get_weekday_display(),
                                 self.from_hour, self.to_hour)

class Gallary(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='gallary')
    photos = models.ImageField(upload_to='companies/gallary/photos', height_field=None, width_field=None, max_length=None)


class Services(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(max_length=200, db_index=True)
    business = models.ForeignKey(Company, related_name='services_offered', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200,db_index=True)
    price_type = models.CharField(max_length=10, choices=price_choices, default='fixed')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_hour = models.IntegerField(choices=hours_choices,default=0)
    duration_minute = models.IntegerField(choices=minute_choices,default=5)
    checkintime = models.IntegerField(choices=minute_choices,default=0)
    paddingtime_hour = models.IntegerField(choices=hours_choices,default=0)
    paddingtime_minute = models.IntegerField(choices=minute_choices,default=0)
    padding = models.CharField(max_length=20,choices=beforeafter, default='none')
    available = models.BooleanField(default=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'service'
        verbose_name_plural = 'services'
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("business:company_detail", args=[self.id, self.slug])

class Amenities(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE)
    amenity = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Amenity'
        verbose_name_plural = 'Amenities'
