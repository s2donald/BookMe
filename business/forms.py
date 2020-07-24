from django import forms
from .models import Category, Services
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
    Search = forms.CharField(label='Search Business or Service',widget=forms.TextInput(attrs={'class':'form-control border border','placeholder':'Search Business or Service'}))
    
class AddServiceForm(forms.Form):
    name = forms.CharField(label='Service Name')
    description = forms.CharField(label='Details Of Service',max_length=30, required=True, widget=forms.Textarea(attrs={'rows':2, 'cols':20}))
    price_type = forms.ChoiceField(label='Price Type',choices=price_choices)
    price = forms.DecimalField(label='Price ($)',max_digits=10, required=True)
    duration_hour = forms.ChoiceField(label='Duration',choices=hours_choices)
    duration_minute = forms.ChoiceField(label='',choices=minute_choices)
    checkintime = forms.ChoiceField(label='Check In Time',choices=minute_choices)
    padding = forms.ChoiceField(label='Padding',choices=beforeafter)
    paddingtime_hour = forms.ChoiceField(label='Padding Time',choices=hours_choices)
    paddingtime_minute = forms.ChoiceField(label='',choices=minute_choices)
    class Meta:
        model = Services
        fields = ('name','description','price_type','price','available','duration_hour',
        'checkintime','padding','paddingtime_hour','paddingtime_minute')

class UpdateServiceForm(forms.Form):
    name = forms.CharField(label='Service Name')
    description = forms.CharField(label='Details Of Service',max_length=30, required=True, widget=forms.Textarea(attrs={'rows':2, 'cols':20}))
    price_type = forms.ChoiceField(label='Price Type',choices=price_choices)
    price = forms.DecimalField(label='Price ($)',max_digits=10, required=True)
    duration_hour = forms.ChoiceField(label='Duration',choices=hours_choices)
    duration_minute = forms.ChoiceField(label='',choices=minute_choices)
    checkintime = forms.ChoiceField(label='Check In Time',choices=minute_choices)
    padding = forms.ChoiceField(label='Padding',choices=beforeafter)
    paddingtime_hour = forms.ChoiceField(label='Padding Time',choices=hours_choices)
    paddingtime_minute = forms.ChoiceField(label='',choices=minute_choices)
    class Meta:
        model = Services
        fields = ('name','description','price_type','price','available','duration_hour','duration_minute',
        'checkintime','padding','paddingtime_hour','paddingtime_minute')