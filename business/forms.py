from django import forms
from .models import Category, Services

class SearchForm(forms.Form):
    Search = forms.CharField(label='Search Business or Service',widget=forms.TextInput(attrs={'class':'form-control border border','placeholder':'Search Business or Service'}))
    
class AddServiceForm(forms.Form):
    name = forms.CharField(label='Service Name')
    description = forms.CharField(label='Details Of Service',max_length=30, required=True)
    price = forms.DecimalField(label='Price ($)',max_digits=10, required=True)
    class Meta:
        model = Services
        fields = ('name','description','price','available')

class UpdateServiceForm(forms.Form):
    name = forms.CharField(label='Service Name')
    description = forms.CharField(label='Details Of Service',max_length=30, required=True)
    price = forms.DecimalField(label='Price ($)',max_digits=10, required=True)
    class Meta:
        model = Services
        fields = ('name','description','price','available')