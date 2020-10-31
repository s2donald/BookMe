from account.models import Account
from business.models import Company, OpeningHours, Gallary, Services
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator
from django.db import models

from business.models import Company, Category, SubCategory
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
minute_choices_no_zero = (
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

class CreateSmallBizForm(forms.Form):
    business_name = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Business Email', required=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = forms.CharField(label='Business Phone Number', validators=[phone_regex], required=True, max_length=30,)

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
        fields = ('business_name','phone','category','description', 'address', 'postal', 'state', 'city', 'fb_link','twitter_link', 'instagram_link', 'website_link')
    def save(self):
        company = super().save(commit=False)
        company.save()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=self.initial['category'].id)
        except AttributeError:
            pass

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory.order_by('name')


from business.models import Clients

class AddClientForm(forms.ModelForm):
    first_name = forms.CharField(label='',max_length=30, required=True)
    last_name = forms.CharField(label='',max_length=30, required=True, widget=forms.TextInput(attrs={}))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = forms.CharField(label='Phone Number',required=False, validators=[phone_regex], max_length=30,widget=forms.TextInput(attrs={}))
    email = forms.EmailField(label='',required=False, widget=forms.TextInput(attrs={}))
    address = forms.CharField(label='', required=False,max_length=35,widget=forms.TextInput(attrs={}))
    province = forms.CharField(label='', required=False,max_length=35,widget=forms.TextInput(attrs={}))
    postal = forms.CharField(label='', required=False,max_length=35,widget=forms.TextInput(attrs={}))
    city = forms.CharField(label='', required=False,max_length=35,widget=forms.TextInput(attrs={}))
    class Meta:
        model = Clients
        fields = ('first_name','last_name','phone','email','address','province','postal','city')

class AddNotesForm(forms.ModelForm):
    notes = forms.CharField(label='', max_length=250,required=False, widget=forms.Textarea(attrs={'rows':4,'cols':20}))
    class Meta:
        model = Company
        fields = ('notes',)

class AddHoursForm(forms.ModelForm):
    dayto = forms.TimeField(label='', required=True, widget=forms.TextInput(attrs={'class':'datetimepicker form-control text-center'}))
    dayfrom = forms.TimeField(label='', required=True, widget=forms.TextInput(attrs={'class':'datetimepicker form-control text-center'}))
    class Meta:
        model = OpeningHours
        fields = ('from_hour', 'to_hour')

class ImagesForm(forms.ModelForm):
    class Meta:
        model = Gallary
        fields = ('photos',)
        widgets = {
            'photos':forms.HiddenInput
        }
    
class AddBookingForm(forms.Form):
    service = forms.ModelChoiceField(queryset=Services.objects.all(),label='Service:', empty_label=None, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control','title':'Service','data-size':'6'}))
    clients = forms.ModelChoiceField(queryset=Clients.objects.all(),label='Client:', empty_label=None, required=False, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control','title':'Select Client','data-size':'6'}))
    timepick = forms.TimeField(label='Time',required=True, widget=forms.TextInput(attrs={'class':'form-control timepicker'}))
    datepick = forms.DateField(label='Date', required=True, widget=forms.TextInput(attrs={'class':'form-control datepicker'}))
    price = forms.DecimalField(label='Price ($)',max_digits=10, required=True, widget=forms.TextInput(attrs={'type':'number'}))
    duration_hour = forms.ChoiceField(label='Duration Hour',choices=hours_choices, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    duration_minute = forms.ChoiceField(label='Duration Minute',choices=minute_choices,initial= '30', widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    # search = forms.CharField(label='Search Business',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Search Business or Service','list':'clients'}))

    first_name = forms.CharField(label='First Name',max_length=30, required=True)
    last_name = forms.CharField(label='Last Name',max_length=30, required=True, widget=forms.TextInput(attrs={}))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = forms.CharField(label='Phone Number',required=False, validators=[phone_regex], max_length=30,widget=forms.TextInput(attrs={}))
    email = forms.EmailField(label='Email',required=False, widget=forms.TextInput(attrs={}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Services.objects.filter(business=self.initial['company'].id).order_by('name')
        self.fields['clients'].queryset = Clients.objects.filter(company=self.initial['company'].id).order_by('first_name')

        

