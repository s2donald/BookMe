from account.models import Account
from products.models import addOnProducts, Product
from business.models import Company, OpeningHours, Gallary, Services, ServiceCategories
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator
from django.db import models
import re
from business.models import Company, Category, SubCategory
from calendarapp.models import formBuilder


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