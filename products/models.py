from django.db import models
from business.models import Company
from gibele.utils import unique_slug_generator_product, unique_slug_generator_addonproduct
from django.db.models.signals import pre_save
from django.utils import timezone
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
class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(max_length=250, db_index=True)
    business = models.ForeignKey(Company, related_name='products_offered', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200,db_index=True,blank=True, unique=True)
    currency = models.CharField(choices=currencychoice, max_length=200,db_index=True,default="CA")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    request = models.BooleanField(default=False)
    mainimage = models.ImageField(upload_to=get_product_image_folder, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'products'
        verbose_name_plural = 'products'
    def __str__(self):
        return self.name

def slug_generators(sender, instance, *args, **kwargs):
    print('yea')
    if not instance.slug:
        instance.slug = unique_slug_generator_product(instance)

pre_save.connect(slug_generators, sender=Product)

class addOnProducts(models.Model):
    product = models.ForeignKey(Product, related_name='addon_product', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=200,db_index=True,blank=True, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    mainimage = models.ImageField(upload_to=get_addon_image_folder, blank=True)

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