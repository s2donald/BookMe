from account.models import Account
from business.models import Company
from account.tasks import bizaddedEmailSent
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator
from django.db import models

from business.models import Company, Category, SubCategory

class BusinessRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='First Name', required=True, max_length=30)
    last_name = forms.CharField(label='Last Name', required=True, max_length=30)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = forms.CharField(label='Business Phone Number', validators=[phone_regex], required=True, max_length=30,)
    email = forms.EmailField(label='Business Email')
    prefix = 'businessregistration'
    class Meta:
        model = Account
        fields = ('first_name','last_name','email', 'phone', 'password1', 'password2')

    def save(self):
        user = super().save(commit=False)
        user.is_business = True
        user.save()

    def clean_email(self):
        email = self.cleaned_data['email']
        acct = Account.objects.filter(email=email)
        if acct:
            raise forms.ValidationError("Email address is already in use.")
            
        return email

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

from PIL import Image
from django import forms
from django.core.files import File

class MainPhoto(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Company
        fields = ('image', 'x', 'y', 'width', 'height', )

    def save(self):
        photo = super(MainPhoto, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        images = Image.open(photo.image)
        cropped_image = images.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.image.path)

        return photo


class UpdateCompanyForm(forms.ModelForm):
    business_name = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='', required=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all(),label='', empty_label=None, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control','title':'Category'}))
    subcategory = forms.ModelMultipleChoiceField(queryset=SubCategory.objects.all(),label='', widget=forms.SelectMultiple(attrs={'class':'selectcolor selectpicker show-tick form-control','multiple':'', 'data-size':'5', 'data-dropdown-align-right':'true', 'title':'Subcategories'}))
    description = forms.CharField(label='', max_length=500,required=False, widget=forms.Textarea(attrs={'rows':4,'cols':20}))
    address = forms.CharField(label='', max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = forms.CharField(label='', validators=[phone_regex], required=False, max_length=30)
    postal_regex = RegexValidator(regex=r"^[ABCEGHJKLMNPRSTVXY]{1}\d{1}[A-Z]{1} *\d{1}[A-Z]{1}\d{1}$")
    postal = forms.CharField(max_length=10, validators=[postal_regex], label='', required=True, error_messages={'invalid': 'Enter a valid Postal Code or ZIP Code.'}, widget=forms.TextInput(attrs={'class':'form-control'}))
    state = forms.CharField(max_length=2, label='', required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    city = forms.CharField(max_length=30,label='',required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    website_link = forms.URLField(max_length=200, label='', required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    instagram_link = forms.URLField(max_length=200, label='', required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    fb_link = forms.URLField(max_length=200, label='', required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    twitter_link = forms.URLField(max_length=200, label='', required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    prefix = 'updatecompany'
    class Meta:
        model = Company
        fields = ('business_name','phone','category', 'description', 'address', 'postal', 'state', 'city', 'fb_link','twitter_link', 'instagram_link', 'website_link')
    def save(self):
        company = super().save(commit=False)
        company.save()


from business.models import Clients

class AddClientForm(forms.ModelForm):
    first_name = forms.CharField(label='',max_length=30, required=True, widget=forms.TextInput(attrs={'style':'color:black;'}))
    last_name = forms.CharField(label='',max_length=30, required=True, widget=forms.TextInput(attrs={'style':'color:black;'}))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = forms.CharField(label='Phone Number',required=False, validators=[phone_regex], max_length=30,widget=forms.TextInput(attrs={'style':'color:black;'}))
    email = forms.EmailField(label='',widget=forms.TextInput(attrs={'style':'color:black;'}))
    address = forms.CharField(label='', max_length=35,widget=forms.TextInput(attrs={'style':'color:black;'}))
    province = forms.CharField(label='', max_length=35,widget=forms.TextInput(attrs={'style':'color:black;'}))
    postal = forms.CharField(label='', max_length=35,widget=forms.TextInput(attrs={'style':'color:black;'}))
    city = forms.CharField(label='', max_length=35,widget=forms.TextInput(attrs={'style':'color:black;'}))
    class Meta:
        model = Clients
        fields = ('first_name','last_name','phone','email','address','province','postal','city')
