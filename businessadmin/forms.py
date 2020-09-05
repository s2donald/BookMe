from account.models import Account
from business.models import Company
from account.tasks import bizaddedEmailSent
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator


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