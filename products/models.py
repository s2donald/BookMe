from django.db import models
from business.models import Company, Clients, CompanyReq
from gibele.utils import unique_slug_generator_product, unique_slug_generator_order
from django.db.models.signals import pre_save
from django.utils import timezone
from account.models import Account
from django.core.validators import MinValueValidator, MaxValueValidator,RegexValidator
from address.models import AddressField
from django_countries.fields import CountryField
from cities.models import City, Region
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
typeofchoice = (
    (0, "Free text"),
    (1, 'Image Attachment')
)

day = (
    (0, 'Ready for delivery right away'),
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


class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    description = HTMLField(null=True, blank=True)
    business = models.ForeignKey(Company, related_name='products_offered', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200,db_index=True, unique=True)
    currency = models.CharField(choices=currencychoice, max_length=200,db_index=True,default="CA")
    price = models.DecimalField(verbose_name="Base Price",max_digits=10, decimal_places=2)
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
        unique_together=(('business','slug'),)
        verbose_name = 'products'
        verbose_name_plural = 'products'
    def __str__(self):
        return f'{self.name} - {self.business}'

def slug_generators(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_product(instance)

pre_save.connect(slug_generators, sender=Product)

class ProductCategory(models.Model):
    name = models.CharField(max_length=200,db_index=True)
    slug = models.SlugField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='product_category', null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)
    class Meta:
        ordering=('name',)
        verbose_name='category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return f'{self.name} - {self.company}'

class GallaryProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='product_gallary', on_delete=models.CASCADE)
    photos = models.ImageField(upload_to='companies/gallary/product/photos')
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created',)

class MainProductDropDown(models.Model):
    product = models.ForeignKey(Product, related_name='product_maindropdown', on_delete=models.CASCADE)
    placeholder = models.CharField(max_length=200, db_index=True)
    sublabel = models.CharField(max_length=200, default="", null=True, blank=True)
    is_required = models.BooleanField(default=True)
    is_multiple = models.BooleanField(default=True)

class ProductDropDown(models.Model):
    option = models.CharField(max_length=200, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    dropdown = models.ForeignKey(MainProductDropDown, related_name='main_dropdown', on_delete=models.CASCADE)
    def __str__(self):
        return f'Extra {self.option} - {self.dropdown.product.business}'

class QuestionModels(models.Model):
    question = models.CharField(max_length=400, db_index=True)
    placeholder = models.CharField(max_length=400, null=True, blank=True)
    is_required = models.BooleanField(default=False)
    retrievetype = models.IntegerField(choices=typeofchoice, default=0, verbose_name='Get it in a form of:')
    product = models.ForeignKey(Product, related_name='product_questions', on_delete=models.CASCADE)


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


class Order(models.Model):
    company = models.ForeignKey(Company, related_name='orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField("Phone Number", max_length=17, null=True, blank=True)
    address = models.CharField(verbose_name="Address", max_length=200, null=True, blank=True)
    country = CountryField(blank=True, null=True)
    postal_code = models.CharField(max_length=20)
    slug = models.SlugField(max_length=200,db_index=True, unique=True)
    city = models.CharField(max_length=100)
    state = models.ForeignKey(Region, blank=True, null=True, on_delete=models.CASCADE, verbose_name='State or Province')
    created = models.DateTimeField(auto_now_add=True)
    dateshipped = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    paid = models.BooleanField(default=False)
    orderplaced = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    pendingapproval = models.BooleanField(default=True)
    cancelled = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)

    recieveupdates = models.BooleanField(default=True)


    shipping_local = models.BooleanField(default=False)
    shipping_international = models.BooleanField(default=False)
    paymentintent = models.CharField(verbose_name="Payment Intent", max_length=200, unique=True, null=True, blank=True)
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return f'Order {self.id}'
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    company = models.ForeignKey(Company, related_name='order_items_company', on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50, null=True, blank=True)
    dropdown = models.ManyToManyField(ProductDropDown, related_name='order_addon_extra', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return str(self.id)
    def get_cost(self):
        return self.price * self.quantity
    
def slug_generators_order(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_order(instance)

pre_save.connect(slug_generators_order, sender=Order)

class AnswerModels(models.Model):
    description = HTMLField()
    question = models.ForeignKey(QuestionModels, related_name='client_questionresponse', on_delete=models.CASCADE)
    orderitem = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='answer_orderitems')
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created',)

class MultipleImageOrderAttachments(models.Model):
    answer = models.ForeignKey(AnswerModels, related_name='answer_imageattachments', on_delete=models.CASCADE)
    photos = models.ImageField(upload_to='companies/answers/orders/photos', blank=True)
    orderitem = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='imageattachment_orderitems')
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created',)