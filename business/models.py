from django.contrib.gis.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from django.core.validators import RegexValidator
from account.models import Account, MyAccountManager
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from gibele.utils import unique_slug_generator, unique_slug_generator_services
import geocoder
import pytz
ALL_TIMEZONES = sorted((item, item) for item in pytz.all_timezones)
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
        ordering = ('category',)
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

cancellationtime = (
    (0,'Anytime'),
    (1, '1 hour'),
    (3, '3 hours'),
    (6, '6 hours'),
    (8, '8 hours'),
    (12, '12 hours'),
    (24, '1 day'),
    (48, '2 days'),
    (72, '3 days'),
    (96, '4 days'),
    (168, '1 week'),
    (10000, 'never'),
)

def get_user_image_folder(instance, filename):
    return "company/images/user_{0}/imagefolder/{1}/".format(instance.user.id, filename)

def get_user_image_folder(instance, filename):
    return "company/images/user_{0}/requested/{1}/".format(instance.user.id, filename)

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
    description = models.TextField(max_length=500, db_index=True, blank=True, null=True)
    address = models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    email = models.EmailField(verbose_name='Business Email', max_length=60)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField("Business Phone Number",validators=[phone_regex], max_length=17)
    postal_regex = RegexValidator(regex=r"^[ABCEGHJKLMNPRSTVXYabcdefghijklmnopqrstuvwxyz]{1}\d{1}[A-Z]{1} *\d{1}[A-Z]{1}\d{1}$", message="A valid postal code/ZIP Code must be entered, letters must be in all caps")
    postal = models.CharField(max_length=10, validators=[postal_regex])
    state = models.CharField(max_length=2)
    city = models.CharField(max_length=30)
    slug = models.SlugField(max_length=200, db_index=True, blank=True, unique=True)
    notes = models.TextField(max_length=250, blank=True, null=True)
    returning = models.BooleanField(default=False)
    cancellation = models.IntegerField(choices=cancellationtime, default='0')
    interval = models.IntegerField(choices=INTERVAL, default=1)
    image = models.ImageField(upload_to=get_user_image_folder, blank=True)
    emailReminders = models.BooleanField(default=True)
    confirmation_minutes = models.IntegerField(choices=minute_choices,default=15)
    shownotes = models.BooleanField(default=False)
    users_like = models.ManyToManyField(Account, related_name='companies_liked', blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(default=timezone.now)
    fb_link = models.URLField(max_length=200, blank=True, null=True)
    instagram_link = models.URLField(max_length=200, blank=True, null=True)
    twitter_link = models.URLField(max_length=200, blank=True, null=True)
    website_link = models.URLField(max_length=200, blank=True, null=True)
    tags = TaggableManager(blank=True)
    location = models.PointField(blank=True, null=True)
    tz = models.CharField(choices=ALL_TIMEZONES, max_length=64, default="America/Toronto")
    showAddress = models.BooleanField(default=True)
    class Meta:
        ordering = ('-updated',)
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

def location_update(sender, instance, *args, **kwargs):
    address = instance.address
    if not address:
        g = geocoder.ipinfo('me')
    else:
        g = geocoder.google(address + "," + instance.city,key="AIzaSyBaZM_O3d1-xDrecS_fbcbvoT5qDmLmje0")
    lat = g.latlng[0]
    lng = g.latlng[1]
    instance.location = "POINT(" + str(lng) + " " + str(lat) +")"
    
pre_save.connect(slug_generator, sender=Company)
pre_save.connect(location_update, sender=Company)

class Clients(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='clients')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='company_booked',null=True, blank=True)
    first_name = models.CharField(verbose_name="First Name", max_length=30, unique=False)
    last_name = models.CharField(verbose_name="Last Name", max_length=30, unique=False,null=True, blank=True)
    email = models.EmailField(verbose_name='Email', max_length=60)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17,null=True, blank=True)
    address = models.CharField(max_length=200,null=True, blank=True)
    postal = models.CharField(max_length=35,null=True, blank=True)
    province = models.CharField(max_length=35,null=True, blank=True)
    city = models.CharField(max_length=35,null=True, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
from django.utils.timezone import now
#This model should include all requests for bookings or getting on the client list(Bookings not added yet)
class CompanyReq(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='requests')
    company = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='reqclients')
    created_at = models.DateTimeField(auto_now_add=True)
    add_to_list = models.BooleanField(default=False)

    #To be implemented in the near future, the client can add a description and an image to requested
    description = models.CharField(max_length=400,blank=True)
    image = models.ImageField(upload_to=get_user_image_folder, blank=True)
    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Request For Company'



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
    photos = models.ImageField(upload_to='companies/gallary/photos')

class Services(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(max_length=250, db_index=True)
    business = models.ForeignKey(Company, related_name='services_offered', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200,db_index=True)
    price_type = models.CharField(max_length=10, choices=price_choices, default='fixed')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_hour = models.IntegerField(choices=hours_choices,default=0)
    duration_minute = models.IntegerField(choices=minute_choices,default=30)
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

def slug_generators(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_services(instance)

pre_save.connect(slug_generators, sender=Services)

class Amenities(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE)
    amenity = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Amenity'
        verbose_name_plural = 'Amenities'
