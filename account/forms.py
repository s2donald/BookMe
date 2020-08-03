from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Account
from business.models import Company
from django.core.validators import RegexValidator
from bootstrap_modal_forms.forms import BSModalModelForm

class ConsumerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = forms.CharField(label='Phone Number', validators=[phone_regex], required=True, max_length=30,)
    email = forms.EmailField(label='Email')

    class Meta:
        model = Account
        fields = ('email', 'first_name','last_name', 'phone', 'password1', 'password2')

    def save(self):
        user = super().save(commit=False)
        user.is_consumer = True
        user.save()

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

class UpdateNameForm(forms.Form):
    first_name = forms.CharField(label='First Name',max_length=30)
    last_name = forms.CharField(label='Last Name',max_length=30)
    
    class Meta:
        model = Account
        fields = ('first_name','last_name')

class UpdateEmailForm(forms.ModelForm):
    email = forms.EmailField(label='Email')
    
    class Meta:
        model = Account
        fields = ('email',)

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     try:
    #         match = Account.objects.get(email=email)
    #     except Account.DoesNotExist:
    #         return email
    #     raise forms.ValidationError('This email address is already in use.')

class UpdatePhoneForm(forms.Form):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = forms.CharField(label='Phone Number', validators=[phone_regex], required=True, max_length=30)
    
    class Meta:
        model = Account
        fields = ('phone')

class UpdateHomeAddressForm(forms.Form):
    address = forms.CharField(label='Home Address', max_length=30)

    class Meta:
        model = Account
        fields = ('address')