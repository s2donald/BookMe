from django.db import models
from business.models import Company, Services
from consumer.models import Bookings
from businessadmin.models import StaffMember
from django.core.exceptions import ValidationError
# Create your models here.
yesno = (
        ('y', 'Yes'),
        ('n', 'No')
)
class formBuilder(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_forms')
    services = models.ManyToManyField(Services, related_name='service_forms', blank=True)
    label = models.CharField(max_length=100, db_index=True)
    is_checkbox = models.CharField(max_length=3,default='n', choices=yesno)
    is_text = models.CharField(max_length=3,default='y', choices=yesno)
    order = models.PositiveIntegerField(default=1)
    is_integer = models.CharField(max_length=3,default='n', choices=yesno)
    is_required = models.CharField(max_length=3,default='n', choices=yesno)
    class Meta:
        ordering = ["label"]
    def __str__(self):
        return self.label
    def clean(self):
        if ((self.is_text == 'y') and (self.is_checkbox == 'y')) or ((self.is_checkbox  == 'y') and (self.is_integer  == 'y')) or ((self.is_text  == 'y') and (self.is_integer  == 'y')):
            raise ValidationError('You must select only one option to continue')

        if (self.is_text == 'n') and (self.is_checkbox  == 'n') and (self.is_integer  == 'n'):
            raise ValidationError('You must select only one option to continue')

# def slug_generators(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = unique_slug_generator_staff(instance)
# pre_save.connect(slug_generators, sender=StaffMember)

class bookingForm(models.Model):
    booking = models.ForeignKey(Bookings, on_delete=models.CASCADE, related_name='booking_forms')
    label = models.CharField(max_length=100, blank=True, null=True)
    text = models.CharField(max_length=100, null=True,blank=True)
    integer = models.IntegerField(null=True,blank=True)
    checkbox = models.BooleanField(default=False)





