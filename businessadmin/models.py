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
from gibele.utils import unique_slug_generator, unique_slug_generator_services
import geocoder
import pytz

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
    return "company/other/staff_{0}/calendar/{1}/".format(instance.user.id,"calendar.ics")

class StaffMember(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='staffmembers')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True, related_name='working_for')
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

    class Meta:
        ordering = ('user',)
        verbose_name = 'Staff Member'
    
    def __str__(self):
        if self.first_name==None:
            return "ERROR-Staff NAME IS NULL"
        return self.first_name

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

    

