from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.core.validators import RegexValidator
from django.utils.text import slugify
from django.shortcuts import reverse
# from business.models import Company
# Create your models here.

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
    address = models.CharField(max_length=200)
    postal = models.CharField(max_length=35)
    province = models.CharField(max_length=35)
    city = models.CharField(max_length=35)
    avatar = models.ImageField(upload_to='users/profilepic/', blank=True)

    is_business= models.BooleanField(default=False)
    on_board= models.BooleanField(default=False)
    is_consumer= models.BooleanField(default=False)
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

