from account.models import Account
# from products.models import addOnProducts, Product
from business.models import Company, OpeningHours, Gallary, Services, ServiceCategories, Clients
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator
from django.db import models
import re
from business.models import Company, Category, SubCategory
from calendarapp.models import formBuilder
from consumer.models import AddOnServices
hours_choices = (
        ('0','0 hours'),
        ('1', '1 hour'),
        ('2', '2 hours'),
        ('3', '3 hours'),
        ('4', '4 hours'),
        ('5', '5 hours'),
        ('6', '6 hours'),
        ('7', '7 hours'),
        ('8', '8 hours'),
        ('9', '9 hours'),
        ('10', '10 hours'),
        ('11', '11 hours'),
        ('12', '12 hours'),
        ('13', '13 hours'),
        ('14', '14 hours'),
        ('15', '15 hours'),
        ('16', '16 hours'),
        ('17', '17 hours'),
        ('18', '18 hours'),
        ('19', '19 hours'),
        ('20', '20 hours'),
        ('21', '21 hours'),
        ('22', '22 hours'),
        ('23', '23 hours')
    )

minute_choices = (
        ('0', '0 minutes'),
        ('5', '5 minutes'),
        ('10', '10 minutes'),
        ('15', '15 minutes'),
        ('20', '20 minutes'),
        ('25', '25 minutes'),
        ('30', '30 minutes'),
        ('35', '35 minutes'),
        ('40', '40 minutes'),
        ('45', '45 minutes'),
        ('50', '50 minutes'),
        ('55', '55 minutes')
    )
# class InitialCartSetup(forms.ModelForm):
#     product = forms.ModelChoiceField(queryset=Product.objects.none(),label='', empty_label=None, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control','title':'Category'}))
    
#     class Meta:
#         model = addOnProducts
#         fields = ('product')
#     def save(self):
#         company = super().save(commit=False)
#         company.save()
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         try:
#             self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=self.initial['category'].id)
#         except AttributeError:
#             pass

#         if 'category' in self.data:
#             try:
#                 category_id = int(self.data.get('category'))
#                 self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
#             except (ValueError, TypeError):
#                 pass
#         elif self.instance.pk:
#             self.fields['subcategory'].queryset = self.instance.category.subcategory.order_by('name')


# class AddBookingForm(forms.Form):
#     service = forms.ModelChoiceField(queryset=Services.objects.all(),label='Service:', empty_label=None, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control','title':'Service','data-size':'6','data-live-search':"true", 'data-live-search-placeholder':"Search Services"}))
#     clients = forms.ModelChoiceField(queryset=Clients.objects.all(),label='Client:', empty_label=None, required=False, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control','title':'Select Client','data-size':'6','data-live-search':"true", 'data-live-search-placeholder':"Search from client list"}))
#     timepick = forms.TimeField(label='Time',required=True, widget=forms.TextInput(attrs={'class':'form-control timepicker'}))
#     datepick = forms.DateField(label='Date', required=True, widget=forms.TextInput(attrs={'class':'form-control datepicker'}))
#     price = forms.DecimalField(label='Price ($)',max_digits=10, required=True, widget=forms.TextInput(attrs={'type':'number'}))
#     duration_hour = forms.ChoiceField(label='Duration Hour',choices=hours_choices, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
#     duration_minute = forms.ChoiceField(label='Duration Minute',choices=minute_choices,initial= '30', widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
#     # search = forms.CharField(label='Search Business',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Search Business or Service','list':'clients'}))

#     first_name = forms.CharField(label='First Name',max_length=30, required=True)
#     last_name = forms.CharField(label='Last Name',max_length=30, required=True, widget=forms.TextInput(attrs={}))
#     phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
#     phone = forms.CharField(label='Phone Number',required=False, validators=[phone_regex], max_length=30,widget=forms.TextInput(attrs={}))
#     email = forms.EmailField(label='Email',required=False, widget=forms.TextInput(attrs={}))

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['service'].queryset = Services.objects.filter(business=self.initial['company'].id).order_by('name')
#         self.fields['clients'].queryset = Clients.objects.filter(company=self.initial['company'].id).order_by('first_name')

class AddOnServiceForm(forms.Form):
    name = forms.CharField(label='Add On Service Name', required=True, max_length=60)
    duration_hour = forms.ChoiceField(label='Duration Hour',choices=hours_choices, widget=forms.Select(attrs={'class':' form-control', 'data-size':'5'}))
    duration_minute = forms.ChoiceField(label='Duration Minute',choices=minute_choices,initial= '30', widget=forms.Select(attrs={'class':' form-control', 'data-size':'5'}))
    price = forms.DecimalField(label='Price ($)',max_digits=10, required=True, widget=forms.TextInput(attrs={'type':'number'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields['services'].queryset = Services.objects.filter(company=self.initial['company'].id)
        except AttributeError:
            pass