from django.db import models
from business.models import Company, Services
from django.urls import reverse
from taggit.managers import TaggableManager
from django.core.validators import RegexValidator
from account.models import Account, MyAccountManager
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from gibele.utils import unique_slug_generator, unique_slug_generator_services, unique_slug_generator_staff
import geocoder
import pytz

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

# Create your models here.
WEEKDAYS = [
  (0, ("Sunday")),
  (1, ("Monday")),
  (2, ("Tuesday")),
  (3, ("Wednesday")),
  (4, ("Thursday")),
  (5, ("Friday")),
  (6, ("Saturday")),
]

STAFF_ACCESS = [
    (0, ("Staff Access")),
    (1, ("Receptionist Access")),
    (2, ("Admin Access"))
]

def calendar_staff_folder(instance, filename):
    return "company/other/staff_{0}/calendar/{1}/".format(instance.company.id,"calendar.ics")

def get_staff_image_folder(instance, filename):
    return "company/other/staff_{0}/images/{1}/".format(instance.company.id, filename)

class StaffMember(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='staffmembers')
    user = models.OneToOneField(Account, on_delete=models.CASCADE, blank=True, null=True, related_name='working_for')
    first_name = models.CharField(verbose_name="First Name", max_length=30, unique=False, null=True, blank=True)
    last_name = models.CharField(verbose_name="Last Name", max_length=30, unique=False, null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField("Phone Number",validators=[phone_regex], max_length=17, null=True, blank=True)
    email = models.EmailField(verbose_name='Email', max_length=60, unique=True, null=True, blank=True)
    cc_email = models.EmailField(verbose_name='CC Email', max_length=60, unique=False, null=True, blank=True)
    slug = models.SlugField(max_length=200, db_index=True, blank=True, unique=False)
    login = models.BooleanField(default=False)
    access = models.IntegerField(choices=STAFF_ACCESS, default=0)
    calendarics = models.FileField(upload_to=calendar_staff_folder,null=True, blank=True)
    services = models.ManyToManyField(Services, blank=True)
    image = models.ImageField(upload_to=get_staff_image_folder, blank=True)
    stripe_access_token = models.CharField(verbose_name="Stripe Access Token", max_length=200, unique=True, null=True, blank=True)
    stripe_user_id = models.CharField(verbose_name="Stripe User Id", max_length=200, unique=True, null=True, blank=True)

    class Meta:
        ordering = ('user',)
        verbose_name = 'Staff Member'
    
    def __str__(self):
        if self.first_name==None:
            return "Staff Member"
        return self.first_name

def slug_generators(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_staff(instance)

pre_save.connect(slug_generators, sender=StaffMember)

class Breaks(models.Model):
    staffmember = models.ForeignKey(StaffMember, on_delete=models.CASCADE, related_name='staff_breaks', null=True, blank=True)
    weekday = models.IntegerField(choices=WEEKDAYS)
    from_hour = models.TimeField(default='12:00 PM')
    to_hour = models.TimeField(default='13:00 PM')
    class Meta:
        ordering = ('weekday',)
        verbose_name = 'Break'

    def __str__(self):
        return 'Break on ' + self.get_weekday_display()

class StaffWorkingHours(models.Model):
    staff = models.ForeignKey(StaffMember, on_delete=models.CASCADE, related_name='staff_hours')
    weekday = models.IntegerField(choices=WEEKDAYS)
    from_hour = models.TimeField(default='9:00 AM')
    to_hour = models.TimeField(default='5:00 PM')
    is_off = models.BooleanField(default=False)
    class Meta:
        ordering = ('weekday', 'from_hour')
        unique_together = ('weekday', 'staff')

    def __unicode__(self):
        return u'%s: %s - %s' % (self.get_weekday_display(),
                                 self.from_hour, self.to_hour)

    

