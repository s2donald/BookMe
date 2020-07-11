from django import forms
from .models import Category


class SearchForm(forms.Form):
    Search = forms.CharField(label='Search Business or Service',widget=forms.TextInput(attrs={'class':'form-control border border','placeholder':'Search Business or Service'}))
    
    