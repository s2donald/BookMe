from django import forms
from .models import Category, Services, Company, SubCategory
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
beforeafter = (
        ('none', '-'),
        ('before','Before'),
        ('after','After'),
        ('bf','Before & After')
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

cancellationtime = (
    ('0','Anytime'),
    ('1', '1 hour'),
    ('3', '3 hours'),
    ('6', '6 hours'),
    ('8', '8 hours'),
    ('12', '12 hours'),
    ('24', '1 day'),
    ('48', '2 days'),
    ('72', '3 days'),
    ('168', '1 week'),
    ('10000', 'never'),
)

class SearchForm(forms.Form):
    Search = forms.CharField(label='Search Business or Service',widget=forms.TextInput(attrs={'class':'form-control border','placeholder':'Search Business or Service'}))
    
class homeSearchForm(forms.Form):
    Search = forms.CharField(label='Search Business or Service',widget=forms.TextInput(attrs={'class':'form-control border','placeholder':'Search Business or Service'}))
    Location = forms.CharField(required=False, label='Location',widget=forms.TextInput(attrs={'class':'form-control border','placeholder':'Location'}))

class AddServiceForm(forms.ModelForm):
    name = forms.CharField(label='Service Name', widget=forms.Textarea(attrs={'rows':1, 'cols':20,}))
    description = forms.CharField(label='Details Of Service',max_length=250, required=True, widget=forms.Textarea(attrs={'rows':4, 'cols':20}))
    price_type = forms.ChoiceField(label='Price Type',choices=price_choices, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    price = forms.DecimalField(label='Price ($)',max_digits=10, required=True, widget=forms.TextInput(attrs={'type':'number', 'rows':1, 'cols':20,}))
    duration_hour = forms.ChoiceField(label='Duration Hour',choices=hours_choices, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    duration_minute = forms.ChoiceField(label='Duration Minute',choices=minute_choices_no_zero,initial= '5', widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    checkintime = forms.ChoiceField(label='Check In Time',choices=minute_choices, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    padding = forms.ChoiceField(label='Buffer',choices=beforeafter, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    paddingtime_hour = forms.ChoiceField(label='Buffer Hour',choices=hours_choices, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    paddingtime_minute = forms.ChoiceField(label='Buffer Minute',choices=minute_choices, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    class Meta:
        model = Services
        fields = ('name','description','price_type','price','available','duration_hour',
        'checkintime','padding','paddingtime_hour','paddingtime_minute')

class BookingSettingForm(forms.Form):
    interval = forms.ChoiceField(label='',choices=minute_choices_no_zero,initial= '30', widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5', 'data-dropdown-align-right':'true'}))
    cancellation = forms.ChoiceField(label='',choices=cancellationtime, initial= '0', widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5', 'data-dropdown-align-right':'true'}))
    notes = forms.CharField(label='',max_length=250, required=False, widget=forms.Textarea(attrs={'rows':4, 'cols':20, 'style':'color:black;'}))


class UpdateServiceForm(forms.ModelForm):
    name = forms.CharField(label='Service Name', widget=forms.Textarea(attrs={'rows':1, 'cols':20,}))
    description = forms.CharField(label='Details Of Service',max_length=250, required=True, widget=forms.Textarea(attrs={'rows':4, 'cols':20}))
    price_type = forms.ChoiceField(label='Price Type',choices=price_choices, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    price = forms.DecimalField(label='Price ($)',max_digits=10, required=True, widget=forms.TextInput(attrs={'type':'number', 'rows':1, 'cols':20}))
    duration_hour = forms.ChoiceField(label='Duration Hour',choices=hours_choices, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    duration_minute = forms.ChoiceField(label='Duration Minute',choices=minute_choices,initial= '5', widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    checkintime = forms.ChoiceField(label='Check In Time',choices=minute_choices, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    padding = forms.ChoiceField(label='Buffer',choices=beforeafter, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    paddingtime_hour = forms.ChoiceField(label='Buffer Hour',choices=hours_choices, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    paddingtime_minute = forms.ChoiceField(label='Buffer Minute',choices=minute_choices, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    class Meta:
        model = Services
        fields = ('name','description','price_type','price','available','duration_hour','duration_minute',
        'checkintime','padding','paddingtime_hour','paddingtime_minute')

class AddCompanyForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),label='', empty_label=None, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control','title':'Category'}))
    subcategory = forms.ModelMultipleChoiceField(queryset=SubCategory.objects.all(),label='', widget=forms.SelectMultiple(attrs={'class':'selectcolor selectpicker show-tick form-control','multiple':'', 'data-size':'5', 'data-dropdown-align-right':'true', 'title':'Subcategories'}))
    description = forms.CharField(label='', max_length=500, widget=forms.Textarea(attrs={'style':'color:black;','rows':4,'cols':20}))
    address = forms.CharField(label='', max_length=200, widget=forms.TextInput(attrs={'style':'color:black;','class':'form-control'}))
    postal_regex = RegexValidator(regex=r"^[ABCEGHJKLMNPRSTVXY]{1}\d{1}[A-Z]{1} *\d{1}[A-Z]{1}\d{1}$")
    postal = forms.CharField(max_length=10, validators=[postal_regex], label='', error_messages={'invalid': 'Enter a valid Postal Code or ZIP Code.'}, widget=forms.TextInput(attrs={'style':'color:black;','class':'form-control'}))
    state = forms.CharField(max_length=2, label='', widget=forms.TextInput(attrs={'style':'color:black;','class':'form-control'}))
    city = forms.CharField(max_length=30,label='', widget=forms.TextInput(attrs={'style':'color:black;','class':'form-control'}))
    prefix = 'addcompany'
    class Meta:
        model = Company
        fields = ('category', 'description', 'address', 'postal', 'state', 'city')
    def save(self):
        company = super().save(commit=False)
        company.save()



class AddHoursForm(forms.ModelForm):
    sundayto = forms.TimeField(label='To', required=True)
    sundayfrom = forms.TimeField(label='From', required=True)
    sundayclosed = forms.BooleanField(label='Closed', required=False)


    
        
        