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


class StaffMember(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='staffmembers')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    services = models.ManyToManyField(Services, blank=True)
    is_owner = models.BooleanField(default=False)

    class Meta:
        ordering = ('company',)