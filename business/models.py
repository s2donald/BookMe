from django.contrib.gis.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from django.core.validators import RegexValidator
from account.models import Account, MyAccountManager
# from businessadmin.models import StaffMember
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from gibele.utils import unique_slug_generator, unique_slug_generator_services
import geocoder
import pytz
from timezone_field import TimeZoneField
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

il8nl = ["AF", "AX", "AL", "DZ", "AS", "AD", "AO", "AI", "AQ", "AG", "AR",
"AM", "AW", "AU", "AT", "AZ", "BS", "BH", "BD", "BB", "BY", "BE",
"BZ", "BJ", "BM", "BT", "BO", "BQ", "BA", "BW", "BV", "BR", "IO",
"BN", "BG", "BF", "BI", "CV", "KH", "CM", "CA", "KY", "CF", "TD",
"CL", "CN", "CX", "CC", "CO", "KM", "CG", "CD", "CK", "CR", "CI",
"HR", "CU", "CW", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG",
"SV", "GQ", "ER", "EE", "ET", "FK", "FO", "FJ", "FI", "FR", "GF",
"PF", "TF", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GD",
"GP", "GU", "GT", "GG", "GN", "GW", "GY", "HT", "HM", "VA", "HN",
"HK", "HU", "IS", "IN", "ID", "IR", "IQ", "IE", "IM", "IL", "IT",
"JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KP", "KR", "KW", "KG",
"LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MO", "MK",
"MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT",
"MX", "FM", "MD", "MC", "MN", "ME", "MS", "MA", "MZ", "MM", "NA",
"NR", "NP", "NL", "NC", "NZ", "NI", "NE", "NG", "NU", "NF", "MP",
"NO", "OM", "PK", "PW", "PS", "PA", "PG", "PY", "PE", "PH", "PN",
"PL", "PT", "PR", "QA", "RE", "RO", "RU", "RW", "BL", "SH", "KN",
"LC", "MF", "PM", "VC", "WS", "SM", "ST", "SA", "SN", "RS", "SC",
"SL", "SG", "SX", "SK", "SI", "SB", "SO", "ZA", "GS", "SS", "ES",
"LK", "SD", "SR", "SJ", "SZ", "SE", "CH", "SY", "TW", "TJ", "TZ",
"TH", "TL", "TG", "TK", "TO", "TT", "TN", "TR", "TM", "TC", "TV",
"UG", "UA", "AE", "GB", "US", "UM", "UY", "UZ", "VU", "VE", "VN",
"VG", "VI", "WF", "EH", "YE", "ZM", "ZW"]
il8nlist = sorted((item, item) for item in il8nl)

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
subscriptionplan = (
    (0,'Free'),
    (1, 'Pro'),
    (2, 'Premium'),
)
backgroundstyle = (
    ('primary', 'primary'),
    ('carbon', 'carbon'),
    ('hexagon', 'hexagon'),
)

def get_user_image_folder(instance, filename):
    return "company/images/user_{0}/imagefolder/{1}/".format(instance.user.id, filename)

def get_user_image_folder(instance, filename):
    return "company/images/user_{0}/requested/{1}/".format(instance.user.id, filename)

def calendar_folder(instance, filename):
    return "company/other/user_{0}/calendar/{1}/".format(instance.user.id,"calendar.ics")



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
    postal = models.CharField(max_length=10)
    state = models.CharField(max_length=2)
    city = models.CharField(max_length=30)
    slug = models.SlugField(max_length=200, db_index=True, blank=True, unique=True)
    notes = models.TextField(max_length=250, blank=True, null=True)
    returning = models.BooleanField(default=False)
    background = models.CharField(max_length=200, default='primary', choices=backgroundstyle)
    cancellation = models.IntegerField(choices=cancellationtime, default='0')
    interval = models.IntegerField(choices=INTERVAL, default=1)
    image = models.ImageField(upload_to=get_user_image_folder, blank=True)
    emailReminders = models.BooleanField(default=True)
    confirmation_minutes = models.IntegerField(choices=minute_choices,default=15)
    shownotes = models.BooleanField(default=False)
    calendarics = models.FileField(upload_to=calendar_folder,null=True, blank=True)
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
    darkmode = models.BooleanField(default=False)
    tz = TimeZoneField(default='America/Toronto')
    showAddress = models.BooleanField(default=True)
    subscriptionplan = models.IntegerField(choices=subscriptionplan, default=0)
    

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
    try:
        lat = g.latlng[0]
        lng = g.latlng[1]
        instance.location = "POINT(" + str(lng) + " " + str(lat) +")"
    except TypeError:
        raise ValueError("Must have a valid address")
    
    
pre_save.connect(slug_generator, sender=Company)
pre_save.connect(location_update, sender=Company)

class Clients(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='clients')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='company_booked',null=True, blank=True)
    first_name = models.CharField(verbose_name="First Name", max_length=30, unique=False)
    last_name = models.CharField(verbose_name="Last Name", max_length=30, unique=False,null=True, blank=True)
    email = models.EmailField(verbose_name='Email', max_length=60,null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10,10}$', message="Please enter a 10 digit Phone Number.")
    phone = models.CharField(validators=[phone_regex], max_length=17,null=True, blank=True)
    address = models.CharField(max_length=200,null=True, blank=True)
    phone_code = models.CharField(max_length=2, verbose_name='Phone Code',choices=il8nlist, default="CA", null=True, blank=True)
    postal = models.CharField(max_length=35,null=True, blank=True)
    province = models.CharField(max_length=35,null=True, blank=True)
    city = models.CharField(max_length=35,null=True, blank=True)
    class Meta:
        ordering = ('first_name',)
    def __str__(self):
        if not (self.first_name and self.last_name):
            return 'No Val'
        else:
            return self.first_name + ' ' + self.last_name
    def clean(self):
        if self.phone:
            self.phone = self.phone.strip()


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

class ServiceCategories(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='service_category')
    services = models.ManyToManyField(Services, blank=True)
    def __str__(self):
        return self.name +' Services'

def slug_generators(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_services(instance)

pre_save.connect(slug_generators, sender=Services)

class Amenities(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_amenity')
    amenity = models.CharField(max_length=30)

    def __str__(self):
        return self.amenity

    class Meta:
        verbose_name = 'Amenity'
        verbose_name_plural = 'Amenities'
