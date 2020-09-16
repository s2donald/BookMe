from account.models import Account
from business.models import Company
from account.tasks import bizaddedEmailSent
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator
from django.db import models

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



