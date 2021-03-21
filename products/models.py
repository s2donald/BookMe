from django.db import models
from business.models import Company
# Create your models here.


def get_company_image_folder(instance, filename):
    return "company/images/products/company_{0}/{1}/".format(instance.business.id, filename)

class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(max_length=250, db_index=True)
    business = models.ForeignKey(Company, related_name='products_offered', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200,db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    request = models.BooleanField(default=False)
    mainimage = models.ImageField(upload_to=get_company_image_folder, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'products'
        verbose_name_plural = 'products'
    def __str__(self):
        return self.name

class addOnProducts(models.Model):
    product = models.ForeignKey(Product, related_name='addon_product', on_delete=models.CASCADE)
    description = models.TextField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=200,db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    mainimage = models.ImageField(upload_to=get_company_image_folder, blank=True)

class GallaryProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='product_gallary', on_delete=models.CASCADE)
    photos = models.ImageField(upload_to='companies/gallary/product/photos')