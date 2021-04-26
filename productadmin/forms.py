from account.models import Account
from products.models import Product, MainProductDropDown, ProductDropDown, QuestionModels
from business.models import Company, OpeningHours, Gallary, Services, ServiceCategories
from django import forms
from django.core.validators import RegexValidator
from tinymce.widgets import TinyMCE
from django.conf import settings

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

class AddCompanyForm(forms.ModelForm):
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
        fields = ('description', 'address', 'postal', 'state', 'city')
    def save(self):
        company = super().save(commit=False)
        company.save()

class AddProductForm(forms.ModelForm):
    # description = forms.CharField(widget=TinyMCE(attrs={'cols': 280, 'rows':50,'class': 'form-control'}))
    class Meta:
        model = Product
        fields = ('name','description', 'price', 'mainimage', 'dispatch', 'request')

class dropDownForm(forms.ModelForm):
    placeholder = forms.CharField(label='Dropdown Name', widget=forms.TextInput(attrs={'placeholder': 'What do the options represent? Colors, Sizes, Add Ons, etc'}))
    class Meta:
        model = MainProductDropDown
        fields = ('placeholder', 'is_required', 'is_multiple')

class dropDownOptionsForm(forms.ModelForm):
    option = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Add Option'}))
    class Meta:
        model = ProductDropDown
        fields = ('option', 'price')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].label = ''
        self.fields['price'].widget.attrs['placeholder'] = 'Additional price of the option. (Enter zero if there is no additional cost)'


class questionProductForm(forms.ModelForm):
    question = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Request necessary details such as dimensions, guidelines and more', 'style':'border:1px solid #dadbdd !important; box-shadow: 0 2px 4px rgba(0,0,0,.06); border-radius: 3px;', 'cols':40, 'rows':5, 'size': '40'}))
    placeholder = forms.CharField(label='Placeholder Text', required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter placeholder text for this form field', 'style':'border:1px solid #dadbdd !important; box-shadow: 0 2px 4px rgba(0,0,0,.06); border-radius: 3px;',}))
    class Meta:
        model = QuestionModels
        fields = ('question','placeholder',)