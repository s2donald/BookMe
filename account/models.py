from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.core.validators import RegexValidator
from django.utils.text import slugify
from django.shortcuts import reverse
import pytz
ALL_TIMEZONES = sorted((item, item) for item in pytz.all_timezones)
# from business.models import Company
# Create your models here.
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

class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None, picture=None):
        if not email:
            raise ValueError("Users must have an email address")

        
        user = self.model(
            email = self.normalize_email(email),
        )
        user.avatar = picture
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone=None, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        user.save()
        return user

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email', max_length=60, unique=True)
    first_name = models.CharField(verbose_name="First Name", max_length=30, unique=False,null=True, blank=True)
    last_name = models.CharField(verbose_name="Last Name", max_length=30, unique=False, null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField("Phone Number",validators=[phone_regex], max_length=17, null=True, blank=True)
    phone_code = models.CharField(max_length=2, verbose_name='Phone Code',choices=il8nlist, default="CA", null=True, blank=True)
    address = models.CharField(max_length=200)
    postal = models.CharField(max_length=35)
    province = models.CharField(max_length=35)
    city = models.CharField(max_length=35)
    avatar = models.ImageField(upload_to='users/profilepic/', blank=True)
    tz = models.CharField(choices=ALL_TIMEZONES, max_length=64, default="America/Toronto")

    is_business= models.BooleanField(default=False)
    on_board= models.BooleanField(default=False)
    is_consumer= models.BooleanField(default=True)
    is_guest=models.BooleanField(default=False)

    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    ordering = ('email',)
    REQUIRED_FIELDS = ['phone',]
    objects = MyAccountManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def set_business(self):
        self.is_business = True
        return

    def __str__(self):
        return self.email 

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_perms(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

