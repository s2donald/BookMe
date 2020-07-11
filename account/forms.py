from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Account
from business.models import Company
from django.core.validators import RegexValidator

class ConsumerRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Username', max_length=30)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = forms.CharField(label='Phone Number', validators=[phone_regex], required=True, max_length=30,)
    email = forms.CharField(label='Email')

    class Meta:
        model = Account
        fields = ('username','email', 'first_name','last_name', 'phone', 'password1', 'password2')

    def save(self):
        user = super().save(commit=False)
        user.is_consumer = True
        user.save()

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class BusinessRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    username = forms.CharField(label='Business Name')
    first_name = forms.CharField(label='Business Owner\'s First Name',max_length=30, required=True)
    last_name = forms.CharField(label='Business Owner\'s Last Name',max_length=30, required=True)
    address = forms.CharField(label='Company Address')
    email = forms.CharField(label='Business Email')
    class Meta:
        model = Account
        fields = ('username','first_name','last_name','address','email', 'phone',)
    
    def save(self):
        user = super().save(commit=False)
        user.is_business = True
        user.save()

        address = self.cleaned_data.get('address')
        business = Company.objects.create(user=user, address=address)
        business.save()
        return user

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Please enter a valid Email and Password. Fields are case-sensitive.")