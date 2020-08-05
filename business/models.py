from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from django.core.validators import RegexValidator
from account.models import Account, MyAccountManager
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
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

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')
    
#This is the model for the information we need from each company that is listed on the website
class Company(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='company_page')
    business_name = models.CharField(max_length=30, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='companies', null=True, blank=True)
    description = models.TextField(max_length=200, db_index=True, blank=True)
    address = models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,default='draft')
    postal_regex = RegexValidator(regex=r"^[ABCEGHJKLMNPRSTVXY]{1}\d{1}[A-Z]{1} *\d{1}[A-Z]{1}\d{1}$", message="A valid postal code/ZIP Code must be entered")
    postal = models.CharField(max_length=10, validators=[postal_regex])
    state = models.CharField(max_length=2)
    city = models.CharField(max_length=30)
    slug = models.SlugField(max_length=200, db_index=True, unique_for_date='created')
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

    def get_absolute_url(self):
        return reverse("business:company_detail", args=[self.slug,self.id])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.business_name) 
        super().save(*args, **kwargs)

class Services(models.Model):
    price_choices = (
        ('fixed','Fixed'),
        ('start','Starting Price'),
        ('variable','Variable'),
        ('dont','Don\'t Show'),
        ('free','Free')
    )
    hours_choices = (
        ('zero','0 hours'),
        ('one', '1 hour'),
        ('two', '2 hours'),
        ('three', '3 hours'),
        ('four', '4 hours'),
        ('five', '5 hours'),
        ('six', '6 hours'),
        ('seven', '7 hours'),
        ('eight', '8 hours'),
        ('nine', '9 hours'),
        ('ten', '10 hours'),
        ('eleven', '11 hours'),
        ('twelve', '12 hours'),
        ('thirteen', '13 hours'),
        ('fourteen', '14 hours'),
        ('fifteen', '15 hours'),
        ('sixteen', '16 hours'),
        ('seventeen', '17 hours'),
        ('eighteen', '18 hours'),
        ('nineteen', '19 hours'),
        ('twenty', '20 hours'),
        ('twentyone', '21 hours'),
        ('twentytwo', '22 hours'),
        ('twentythree', '23 hours')
    )

    minute_choices = (
        ('zero', '0 minutes'),
        ('five', '5 minutes'),
        ('ten', '10 minutes'),
        ('fifteen', '15 minutes'),
        ('twenty', '20 minutes'),
        ('twentyfive', '25 minutes'),
        ('thirty', '30 minutes'),
        ('thirtyfive', '35 minutes'),
        ('fourty', '40 minutes'),
        ('fourtyfive', '45 minutes'),
        ('fifty', '50 minutes'),
        ('fiftyfive', '55 minutes')
    )
    beforeafter = (
        ('none', '-'),
        ('before','Before'),
        ('after','After'),
        ('bf','Before & After')
    )
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(max_length=200, db_index=True)
    business = models.ForeignKey(Company, related_name='services_offered', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200,db_index=True)
    price_type = models.CharField(max_length=10, choices=price_choices, default='fixed')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_hour = models.CharField(max_length=11, choices=hours_choices,default='zero')
    duration_minute = models.CharField(max_length=11, choices=minute_choices,default='zero')
    checkintime = models.CharField(max_length=10,choices=minute_choices,default='zero')
    paddingtime_hour = models.CharField(max_length=11,choices=hours_choices,default='zero')
    paddingtime_minute = models.CharField(max_length=10,choices=minute_choices,default='zero')
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