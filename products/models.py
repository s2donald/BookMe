from django.db import models
from business.models import Company, Clients, CompanyReq
from gibele.utils import unique_slug_generator_product, unique_slug_generator_addonproduct
from django.db.models.signals import pre_save
from django.utils import timezone
from account.models import Account
from django.core.validators import MinValueValidator, MaxValueValidator,RegexValidator


# Create your models here.


def get_product_image_folder(instance, filename):
    return "company/images/products/company_{0}/{1}/".format(instance.business.id, filename)

def get_company_image_folder(instance, filename):
    return "company/images/products/company_{0}/{1}/".format(instance.business.id, filename)

def get_addon_image_folder(instance, filename):
    return "company/images/products/addon/company_{0}/{1}/".format(instance.product.id, filename)
currencychoice = (
    ('CA', "CA"),
    ('US', 'US')
)
day = (
    (0, 'Dispatch right away'),
    (1, '1 Day'),
    (2, '2 Days'),
    (3, '3 Days'),
    (4, '4 Days'),
    (5, '5 Days'),
    (6, '6 Days'),
    (7, '7 Days'),
    (8, '8 Days'),
    (9, '9 Days'),
    (10, '10 Days'),
    (11, '11 Days'),
    (12, '12 Days'),
    (13, '13 Days'),
    (14, '14 Days'),
    (15, '15 Days'),
    (16, '16 Days'),
    (17, '17 Days'),
    (18, '18 Days'),
    (19, '19 Days'),
    (20, '20 Days'),
    (21, '21 Days'),
    (22, '22 Days'),
    (23, '23 Days'),
    (24, '24 Days'),
    (25, '25 Days'),
    (26, '26 Days'),
    (27, '27 Days'),
    (28, '28 Days'),
    (29, '29 Days'),
)
from tinymce.models import HTMLField
class ProductCategory(models.Model):
    name = models.CharField(max_length=200,db_index=True)
    slug = models.SlugField(max_length=200,unique=True)
    class Meta:
        ordering=('name',)
        verbose_name='category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, related_name='product_category', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, db_index=True)
    description = HTMLField()
    business = models.ForeignKey(Company, related_name='products_offered', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200,db_index=True, unique=True)
    currency = models.CharField(choices=currencychoice, max_length=200,db_index=True,default="CA")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    request = models.BooleanField(default=False)
    mainimage = models.ImageField(upload_to=get_product_image_folder, blank=True)
    dispatch = models.IntegerField(choices=day, default=0)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    isaddon_required = models.BooleanField(default=True)
    isaddon_multiple = models.BooleanField(default=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'products'
        verbose_name_plural = 'products'
    def __str__(self):
        return self.name

def slug_generators(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_product(instance)

pre_save.connect(slug_generators, sender=Product)

class addOnProducts(models.Model):
    product = models.ForeignKey(Product, related_name='addon_product', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200,db_index=True, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
def slug_generators_addon(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_addonproduct(instance)

pre_save.connect(slug_generators_addon, sender=addOnProducts)

class GallaryProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='product_gallary', on_delete=models.CASCADE)
    photos = models.ImageField(upload_to='companies/gallary/product/photos')
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created',)

class MainProductDropDown(models.Model):
    product = models.ForeignKey(Product, related_name='product_maindropdown', on_delete=models.CASCADE)
    placeholder = models.CharField(max_length=200, db_index=True)
    is_required = models.BooleanField(default=True)
    is_multiple = models.BooleanField(default=True)

class ProductDropDown(models.Model):
    option = models.CharField(max_length=200, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    dropdown = models.ForeignKey(MainProductDropDown, related_name='main_dropdown', on_delete=models.CASCADE)

class ProductReviews(models.Model):
    reviewer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='user_reviews_product', null=True, blank=True)
    guest = models.ForeignKey(Clients, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_reviews')
    review = models.TextField(max_length=500)
    star = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('star',)
        unique_together=(('reviewer','product'),)
        index_together=(('reviewer','product'),)
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'

