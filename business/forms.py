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

minute_choices_no_zero_with_hours = (
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
        ('55', '55 minutes'),
        ('60', '1 hour')
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

day = (
    ('0', '0 Day'),
    ('1', '1 Day'),
    ('2', '2 Days'),
    ('3', '3 Days'),
    ('4', '4 Days'),
    ('5', '5 Days'),
    ('6', '6 Days'),
    ('7', '7 Days'),
    ('8', '8 Days'),
    ('9', '9 Days'),
    ('10', '10 Days'),
    ('11', '11 Days'),
    ('12', '12 Days'),
    ('13', '13 Days'),
    ('14', '14 Days'),
    ('15', '15 Days'),
    ('16', '16 Days'),
    ('17', '17 Days'),
    ('18', '18 Days'),
    ('19', '19 Days'),
    ('20', '20 Days'),
    ('21', '21 Days'),
    ('22', '22 Days'),
    ('23', '23 Days'),
    ('24', '24 Days'),
    ('25', '25 Days'),
    ('26', '26 Days'),
    ('27', '27 Days'),
    ('28', '28 Days'),
    ('29', '29 Days'),
)

month_int_choices = (
    ('0', '0 Month'),
    ('1', '1 Month'),
    ('2', '2 Months'),
    ('3', '3 Months'),
    ('4', '4 Months'),
    ('5', '5 Months'),
    ('6', '6 Months'),
    ('7', '7 Months'),
    ('8', '8 Months'),
    ('9', '9 Months'),
    ('10', '10 Months'),
    ('11', '11 Months'),
    ('12', '12 Months'),
)


states = (
    ("AL", "Alabama"),
    ("AK", "Alaska"),
    ("AS", "American Samoa"),
    ("AZ", "Arizona"),
    ("AR", "Arkansas"),
    ("CA", "California"),
    ("CO", "Colorado"),
    ("CT", "Connecticut"),
    ("DE", "Delaware"),
    ("DC", "District Of Columbia"),
    ("FM", "Federated States Of Micronesia"),
    ("FL", "Florida"),
    ("GA", "Georgia"),
    ("GU", "Guam"),
    ("HI", "Hawaii"),
    ("ID", "Idaho"),
    ("IL", "Illinois"),
    ("IN", "Indiana"),
    ("IA", "Iowa"),
    ("KS", "Kansas"),
    ("KY", "Kentucky"),
    ("LA", "Louisiana"),
    ("ME", "Maine"),
    ("MH", "Marshall Islands"),
    ("MD", "Maryland"),
    ("MA", "Massachusetts"),
    ("MI", "Michigan"),
    ("MI", "Michigan"),
    ("MN", "Minnesota"),
    ("MS", "Mississippi"),
    ("MO", "Missouri"),
    ("MT", "Montana"),
    ("NE", "Nebraska"),
    ("NV", "Nevada"),
    ("NH", "New Hampshire"),
    ("NJ", "New Jersey"),
    ("NM", "New Mexico"),
    ("NY", "New York"),
    ("NC", "North Carolina"),
    ("ND", "North Dakota"),
    ("MP", "Northern Mariana Islands"),
    ("OH", "Ohio"),
    ("OK", "Oklahoma"),
    ("OR", "Oregon"),
    ("PW", "Palau"),
    ("PA", "Pennsylvania"),
    ("PR", "Puerto Rico"),
    ("RI", "Rhode Island"),
    ("SC", "South Carolina"),
    ("SD", "South Dakota"),
    ("TN", "Tennessee"),
    ("TX", "Texas"),
    ("UT", "Utah"),
    ("VT", "Vermont"),
    ("VI", "Virgin Islands"),
    ("VA", "Virginia"),
    ("WA", "Washington"),
    ("WV", "West Virginia"),
    ("WI", "Wisconsin"),
    ("WY", "Wyoming"),
    ("AB", "Alberta"),
    ("BC", "British Columbia"),
    ("MB", "Manitoba"),
    ("NB", "New Brunswick"),
    ("NL", "Newfoundland and Labrador"),
    ("NS", "Nova Scotia"),
    ("NT", "Northwest Territories"),
    ("NU", "Nunavut"),
    ("ON", "Ontario"),
    ("PE", "Prince Edward Island"),
    ("QC", "Québec"),
    ("SK", "Saskatchewan"),
    ("YT", "Yukon")
)
yesno = (
    ('y','Yes'),
    ('n','No')
)

class SearchForm(forms.Form):
    Search = forms.CharField(label='Search Business',widget=forms.TextInput(attrs={'class':'form-control border','placeholder':'Search Business or Service'}))
    lat = forms.DecimalField(max_digits=19, decimal_places=16, required=False)
    lon = forms.DecimalField(max_digits=19, decimal_places=16, required=False)
    
class homeSearchForm(forms.Form):
    Search = forms.CharField(label='Search Business',widget=forms.TextInput(attrs={'class':'form-control border','placeholder':''}))
    Location = forms.CharField(required=False, label='Location',widget=forms.TextInput(attrs={'class':'form-control border','placeholder':'Location'}))
    lat = forms.DecimalField(max_digits=19, decimal_places=16, required=False)
    lon = forms.DecimalField(max_digits=19, decimal_places=16, required=False)

class AddServiceForm(forms.ModelForm):
    name = forms.CharField(label='Service Name', max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(label='Details Of Service',max_length=250, required=True, widget=forms.Textarea(attrs={'rows':4, 'cols':20}))
    is_request = forms.ChoiceField(label='Must be approved by staff before confirming appointment:',choices=yesno, initial='n', widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control'}))
    price_type = forms.ChoiceField(label='Price Type',choices=price_choices, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    price = forms.DecimalField(label='Price ($)',max_digits=10, required=True, widget=forms.TextInput(attrs={'type':'number', 'rows':1, 'cols':20,}))
    duration_hour = forms.ChoiceField(label='Duration Hour',choices=hours_choices,initial= '0', widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    duration_minute = forms.ChoiceField(label='Duration Minute',choices=minute_choices,initial='30', widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    checkintime = forms.ChoiceField(label='Check In Time',choices=minute_choices, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    padding = forms.ChoiceField(label='', choices=beforeafter, widget=forms.Select(attrs={'class':'d-none selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    paddingtime_hour = forms.ChoiceField(label='', choices=hours_choices, widget=forms.Select(attrs={'class':'d-none selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    paddingtime_minute = forms.ChoiceField(label='', choices=minute_choices, widget=forms.Select(attrs={'class':'d-none selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    class Meta:
        model = Services
        fields = ('name','description','price_type','price','available','duration_hour',
        'checkintime','padding','paddingtime_hour','paddingtime_minute')
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if int(self.fields['duration_hour'].initial) > 0:
    #         self.fields['duration_minute'].choices = minute_choices
    #     else:
    #         self.fields['duration_minute'].choices = minute_choices_no_zero
        
    #     if 'duration_hour' in self.data:
    #         try:
    #             dur_hour = int(self.data.get('duration_hour'))
    #             print(dur_hour)
    #             if dur_hour > 0:
    #                 self.fields['duration_minute'].choices = minute_choices
    #             else:
    #                 self.fields['duration_minute'].choices = minute_choices_no_zero
    #         except (ValueError, TypeError):
    #             pass

class BookingSettingForm(forms.Form):
    interval = forms.ChoiceField(label='',required=False,choices=minute_choices_no_zero_with_hours,initial='30', widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5', 'data-dropdown-align-right':'true','data-live-search':"true"}))
    cancellation = forms.ChoiceField(label='', required=False,choices=cancellationtime, initial= '0', widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5', 'data-dropdown-align-right':'true'}))
    notes = forms.CharField(label='',max_length=250, required=False, widget=forms.Textarea(attrs={'rows':4, 'cols':20}))
    before_window_day = forms.ChoiceField(label='',required=False,choices=day, initial= '0', widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5', 'data-dropdown-align-right':'true'}))
    before_window_hour = forms.ChoiceField(label='',required=False,choices=hours_choices, initial= '0', widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5', 'data-dropdown-align-right':'true'}))
    before_window_min = forms.ChoiceField(label='',required=False,choices=minute_choices, initial= '0', widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5', 'data-dropdown-align-right':'true'}))
    after_window_month = forms.ChoiceField(label='',required=False,choices=month_int_choices, initial= '0', widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5', 'data-dropdown-align-right':'true'}))
    after_window_day = forms.ChoiceField(label='',required=False,choices=day, initial=29, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5', 'data-dropdown-align-right':'true'}))

class UpdateServiceForm(forms.ModelForm):
    name = forms.CharField(label='Service Name',max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(label='Details Of Service',max_length=250, required=True, widget=forms.Textarea(attrs={'rows':4, 'cols':20}))
    is_request = forms.ChoiceField(label='Must be approved by staff before confirming appointment:',choices=yesno, initial='n', widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control'}))
    price_type = forms.ChoiceField(label='Price Type',choices=price_choices, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    price = forms.DecimalField(label='Price ($)',max_digits=10, required=True, widget=forms.TextInput(attrs={'type':'number', 'rows':1, 'cols':20}))
    duration_hour = forms.ChoiceField(label='Duration Hour',choices=hours_choices, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    duration_minute = forms.ChoiceField(label='Duration Minute',choices=minute_choices,initial= '30', widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    checkintime = forms.ChoiceField(label='Check In Time',choices=minute_choices, widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    padding = forms.ChoiceField(label='',choices=beforeafter, widget=forms.Select(attrs={'class':'d-none selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    paddingtime_hour = forms.ChoiceField(label='',choices=hours_choices, widget=forms.Select(attrs={'class':'d-none selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    paddingtime_minute = forms.ChoiceField(label='',choices=minute_choices, widget=forms.Select(attrs={'class':'d-none selectcolor selectpicker show-tick form-control', 'data-size':'5'}))
    class Meta:
        model = Services
        fields = ('name','description','price_type','price','available','duration_hour','duration_minute',
        'checkintime','padding','paddingtime_hour','paddingtime_minute')

class AddCompanyForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),label='', widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control','title':'Category'}))
    subcategory = forms.ModelMultipleChoiceField(queryset=SubCategory.objects.all(),label='', widget=forms.SelectMultiple(attrs={'class':'selectcolor selectpicker show-tick form-control','multiple':'', 'data-size':'5', 'data-dropdown-align-right':'true', 'title':'Subcategories'}))
    description = forms.CharField(label='', max_length=500, widget=forms.Textarea(attrs={'rows':4,'cols':20}))
    address = forms.CharField(label='', max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
    postal_regex = RegexValidator(regex=r"^[ABCEGHJKLMNPRSTVXY]{1}\d{1}[A-Z]{1} *\d{1}[A-Z]{1}\d{1}$")
    postal = forms.CharField(max_length=10, label='', error_messages={'invalid': 'Enter a valid Postal Code or ZIP Code.'}, widget=forms.TextInput(attrs={'class':'form-control'}))
    state = forms.ChoiceField(label='',choices=states,initial= 'ON', widget=forms.Select(attrs={'class':'selectcolor selectpicker show-tick form-control', 'data-size':'5', 'data-live-search':"true", 'data-live-search-placeholder':"Search Province or State"}))
    # state = forms.CharField(max_length=2, label='', widget=forms.TextInput(attrs={'class':'form-control'}))
    city = forms.CharField(max_length=30,label='', widget=forms.TextInput(attrs={'class':'form-control'}))
    prefix = 'addcompany'
    class Meta:
        model = Company
        fields = ('category', 'description', 'address', 'postal', 'state', 'city')
    def save(self):
        company = super().save(commit=False)
        company.save()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = SubCategory.objects.all()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory.order_by('name')


class AddressForm(forms.Form):
    address = forms.CharField(label='Address', max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
    postal_regex = RegexValidator(regex=r"^[ABCEGHJKLMNPRSTVXY]{1}\d{1}[A-Z]{1} *\d{1}[A-Z]{1}\d{1}$")
    postal = forms.CharField(max_length=10, validators=[postal_regex], label='', error_messages={'invalid': 'Enter a valid Postal Code or ZIP Code.'}, widget=forms.TextInput(attrs={'class':'form-control'}))
    state = forms.CharField(max_length=2, label='State', widget=forms.TextInput(attrs={'class':'form-control'}))
    city = forms.CharField(max_length=30,label='City', widget=forms.TextInput(attrs={'class':'form-control'}))

class VehicleMakeModelForm(forms.Form):
    make = forms.CharField(label='Vehicle Make',required=True,max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    model = forms.CharField(label='Vehicle Model',required=True,max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    year = forms.DecimalField(label='Vehicle Year',required=True,max_digits=4,decimal_places=0,widget=forms.TextInput(attrs={'class':'form-control'}))


    
        
        