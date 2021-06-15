from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Account, WaitListCustomers
from business.models import Company, Clients
from django.core.validators import RegexValidator
from bootstrap_modal_forms.forms import BSModalModelForm
import re
import pycountry

# il8nl =  ["AF", "AX", "AL", "DZ", "AS", "AD", "AO", "AI", "AQ", "AG", "AR",
# "AM", "AW", "AU", "AT", "AZ", "BS", "BH", "BD", "BB", "BY", "BE",
# "BZ", "BJ", "BM", "BT", "BO", "BQ", "BA", "BW", "BV", "BR", "IO",
# "BN", "BG", "BF", "BI", "CV", "KH", "CM", "CA", "KY", "CF", "TD",
# "CL", "CN", "CX", "CC", "CO", "KM", "CG", "CD", "CK", "CR", "CI",
# "HR", "CU", "CW", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG",
# "SV", "GQ", "ER", "EE", "ET", "FK", "FO", "FJ", "FI", "FR", "GF",
# "PF", "TF", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GD",
# "GP", "GU", "GT", "GG", "GN", "GW", "GY", "HT", "HM", "VA", "HN",
# "HK", "HU", "IS", "IN", "ID", "IR", "IQ", "IE", "IM", "IL", "IT",
# "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KP", "KR", "KW", "KG",
# "LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MO", "MK",
# "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT",
# "MX", "FM", "MD", "MC", "MN", "ME", "MS", "MA", "MZ", "MM", "NA",
# "NR", "NP", "NL", "NC", "NZ", "NI", "NE", "NG", "NU", "NF", "MP",
# "NO", "OM", "PK", "PW", "PS", "PA", "PG", "PY", "PE", "PH", "PN",
# "PL", "PT", "PR", "QA", "RE", "RO", "RU", "RW", "BL", "SH", "KN",
# "LC", "MF", "PM", "VC", "WS", "SM", "ST", "SA", "SN", "RS", "SC",
# "SL", "SG", "SX", "SK", "SI", "SB", "SO", "ZA", "GS", "SS", "ES",
# "LK", "SD", "SR", "SJ", "SZ", "SE", "CH", "SY", "TW", "TJ", "TZ",
# "TH", "TL", "TG", "TK", "TO", "TT", "TN", "TR", "TM", "TC", "TV",
# "UG", "UA", "AE", "GB", "US", "UM", "UY", "UZ", "VU", "VE", "VN",
# "VG", "VI", "WF", "EH", "YE", "ZM", "ZW"]

il8nl = ["CA", "US"]

il8nlist = sorted((item, item) for item in il8nl)
from crispy_forms.helper import FormHelper

class WaitListForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = forms.CharField(label='Phone Number',required=False, validators=[phone_regex], max_length=30,)
    email = forms.EmailField(label='Email')

    class Meta:
        model = WaitListCustomers
        fields = ('email', 'first_name','last_name', 'phone')


class ConsumerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = forms.CharField(label='Phone Number',required=False, validators=[phone_regex], max_length=30,)
    email = forms.EmailField(label='Email')

    class Meta:
        model = Account
        fields = ('email', 'first_name','last_name', 'phone', 'password1', 'password2')

    def save(self):
        user = super().save(commit=False)
        user.is_consumer = True
        user.save()

    def clean_email(self):
        email = self.cleaned_data['email']
        current_email = self.instance.email
        acct = Account.objects.filter(email=email)
        if acct:
            raise forms.ValidationError("Email address is already in use.")
        return email

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        password = cd['password1']
        # calculating the length
        length_error = len(password) < 8
        # searching for digits
        digit_error = re.search(r"\d", password) is None
        # searching for uppercase
        uppercase_error = re.search(r"[A-Z]", password) is None
        # searching for lowercase
        lowercase_error = re.search(r"[a-z]", password) is None
        # searching for symbols
        symbol_error = re.search(r"[ !#?<>:$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None
        # overall result
        password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )
        if not password_ok:
            raise forms.ValidationError("Please enter a stronger password. \nPasswords must be atleast 8 characters long that contains atleast 1 digit, a symbol, uppercase and lower case letters.")
        return cd['password2']

class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    email = forms.EmailField(label='Email')
    # referred = forms.CharField(label='Password')
    
    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Please enter a valid Email and Password. Fields are case-sensitive.")

class AccountAuthenticationFormId(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class':'form-control','id':'emails'}))
    
    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Please enter a valid Email and Password. Fields are case-sensitive.")

class UpdatePersonalForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name',max_length=30)
    last_name = forms.CharField(label='Last Name',max_length=30)
    email = forms.EmailField(label='Email')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = forms.CharField(label='Phone Number', validators=[phone_regex], required=False, max_length=30)
    class Meta:
        model = Account
        fields = ('first_name','last_name','email','phone')

    def clean_email(self):
        email = self.cleaned_data['email']
        acct = Account.objects.filter(email=email).exclude(email=self.instance.email)
        if acct:
            raise forms.ValidationError("Email address is already in use.")
        else:
            return email

class GuestPersonalForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name',max_length=30)
    last_name = forms.CharField(label='Last Name',max_length=30)
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='', required=False, max_length=30)
    phone_code = forms.ChoiceField(label='',choices=il8nlist, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'id':"isocode", 'data-live-search':"true", 'data-size':'5'}))
    class Meta:
        model = Clients
        fields = ('first_name','last_name','email','phone')

    def clean_email(self):
        email = self.cleaned_data['email']
        acct = Account.objects.filter(email=email).exclude(email=self.instance.email)
        if acct:
            raise forms.ValidationError("Email address is already associated with an account.")
        else:
            return email

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        return phone
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)


class UpdateHomeAddressForm(forms.Form):
    address = forms.CharField(label='Home Address', max_length=35)
    province = forms.CharField(label='Province/State', max_length=35)
    postal = forms.CharField(label='Postal Code/ZIP Code', max_length=35)
    city = forms.CharField(label='City', max_length=35)
    class Meta:
        model = Account
        fields = ('address','province','postal','city')