from django import forms
from .models import Category, Services, Company
from django.core.validators import RegexValidator
from bootstrap_modal_forms.forms import BSModalModelForm

STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )
price_choices = (
        ('fixed','Fixed'),
        ('start','Starting Price'),
        ('variable','Variable'),
        ('dont','Don\'t Show'),
        ('free','Free')
    )
hours_choices = (
        ('zero','0 hours'),
        ('one', '1 hour'),
        ('two', '2 hours'),
        ('three', '3 hours'),
        ('four', '4 hours'),
        ('five', '5 hours'),
        ('six', '6 hours'),
        ('seven', '7 hours'),
        ('eight', '8 hours'),
        ('nine', '9 hours'),
        ('ten', '10 hours'),
        ('eleven', '11 hours'),
        ('twelve', '12 hours'),
        ('thirteen', '13 hours'),
        ('fourteen', '14 hours'),
        ('fifteen', '15 hours'),
        ('sixteen', '16 hours'),
        ('seventeen', '17 hours'),
        ('eighteen', '18 hours'),
        ('nineteen', '19 hours'),
        ('twenty', '20 hours'),
        ('twentyone', '21 hours'),
        ('twentytwo', '22 hours'),
        ('twentythree', '23 hours')
    )
beforeafter = (
        ('none', '-'),
        ('before','Before'),
        ('after','After'),
        ('bf','Before & After')
    )

minute_choices = (
        ('zero', '0 minutes'),
        ('five', '5 minutes'),
        ('ten', '10 minutes'),
        ('fifteen', '15 minutes'),
        ('twenty', '20 minutes'),
        ('twentyfive', '25 minutes'),
        ('thirty', '30 minutes'),
        ('thirtyfive', '35 minutes'),
        ('fourty', '40 minutes'),
        ('fourtyfive', '45 minutes'),
        ('fifty', '50 minutes'),
        ('fiftyfive', '55 minutes')
    )

class SearchForm(forms.Form):
    Search = forms.CharField(label='Search Business or Service',widget=forms.TextInput(attrs={'class':'form-control border','placeholder':'Search Business or Service'}))
    
class homeSearchForm(forms.Form):
    Search = forms.CharField(label='Search Business or Service',widget=forms.TextInput(attrs={'class':'form-control border','placeholder':'Search Business or Service'}))
    Location = forms.CharField(required=False, label='Location',widget=forms.TextInput(attrs={'class':'form-control border','placeholder':'Location'}))

class AddServiceForm(forms.ModelForm):
    name = forms.CharField(label='Service Name')
    description = forms.CharField(label='Details Of Service',max_length=30, required=True, widget=forms.Textarea(attrs={'rows':2, 'cols':20}))
    price_type = forms.ChoiceField(label='Price Type',choices=price_choices)
    price = forms.DecimalField(label='Price ($)',max_digits=10, required=True)
    duration_hour = forms.ChoiceField(label='Duration Hour',choices=hours_choices)
    duration_minute = forms.ChoiceField(label='Duration Minute',choices=minute_choices)
    checkintime = forms.ChoiceField(label='Check In Time',choices=minute_choices)
    padding = forms.ChoiceField(label='Padding',choices=beforeafter)
    paddingtime_hour = forms.ChoiceField(label='Padding Hour',choices=hours_choices)
    paddingtime_minute = forms.ChoiceField(label='Padding Minute',choices=minute_choices)
    class Meta:
        model = Services
        fields = ('name','description','price_type','price','available','duration_hour',
        'checkintime','padding','paddingtime_hour','paddingtime_minute')

class UpdateServiceForm(forms.ModelForm):
    name = forms.CharField(label='Service Name')
    description = forms.CharField(label='Details Of Service',max_length=30, required=True, widget=forms.Textarea(attrs={'rows':2, 'cols':20}))
    price_type = forms.ChoiceField(label='Price Type',choices=price_choices)
    price = forms.DecimalField(label='Price ($)',max_digits=10, required=True)
    duration_hour = forms.ChoiceField(label='Duration Hour',choices=hours_choices)
    duration_minute = forms.ChoiceField(label='Duration Minute',choices=minute_choices)
    checkintime = forms.ChoiceField(label='Check In Time',choices=minute_choices)
    padding = forms.ChoiceField(label='Padding',choices=beforeafter)
    paddingtime_hour = forms.ChoiceField(label='Padding Hour',choices=hours_choices)
    paddingtime_minute = forms.ChoiceField(label='Padding Minute',choices=minute_choices)
    class Meta:
        model = Services
        fields = ('name','description','price_type','price','available','duration_hour','duration_minute',
        'checkintime','padding','paddingtime_hour','paddingtime_minute')

class AddCompanyForm(forms.ModelForm):
    business_name = forms.CharField(max_length=30, label='Business Name')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Category')
    description = forms.CharField(label='Brief Business Description', max_length=30, widget=forms.Textarea(attrs={'rows':3,'cols':20}))
    address = forms.CharField(label='Business Address', max_length=200)
    status = forms.ChoiceField(label='Status',choices=STATUS_CHOICES)
    postal_regex = RegexValidator(regex=r"^[ABCEGHJKLMNPRSTVXY]{1}\d{1}[A-Z]{1} *\d{1}[A-Z]{1}\d{1}$")
    postal = forms.CharField(max_length=10, validators=[postal_regex], label='Postal Code/ZIP Code', error_messages={'invalid': 'Enter a valid Postal Code or ZIP Code.'})
    state = forms.CharField(max_length=2, label='Province/State')
    city = forms.CharField(max_length=30,label='City')

    class Meta:
        model = Company
        fields = ('business_name', 'category', 'description', 'address', 'status', 'postal', 'state', 'city')

    
        
        