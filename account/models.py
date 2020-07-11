from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.utils.text import slugify
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, phone, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        if not phone:
            raise ValueError("Users must have a phone number")


        user = self.model(
            email = self.normalize_email(email),
            phone=phone,
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            password=password,
            phone=phone,
            username=username
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        user.save()
        return user
    

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email', max_length=60, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    first_name = models.CharField(verbose_name="First Name", max_length=30, unique=False,null=True, blank=True)
    last_name = models.CharField(verbose_name="Last Name", max_length=30, unique=False, null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField("Phone Number",validators=[phone_regex], max_length=17)
    username = models.CharField(max_length=30, unique=True)
    address = models.CharField(max_length=200) 
    is_business= models.BooleanField(default=False)
    is_consumer= models.BooleanField(default=False)

    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','phone',]
    objects = MyAccountManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def set_business(self):
        self.is_business = True
        return

    def __str__(self):
        return self.username 

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_perms(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
