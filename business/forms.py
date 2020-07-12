from django import forms
from .models import Category, Services

class SearchForm(forms.Form):
    Search = forms.CharField(label='Search Business or Service',widget=forms.TextInput(attrs={'class':'form-control border border','placeholder':'Search Business or Service'}))
    
class AddServiceForm(forms.Form):
    name = forms.CharField(label='Service Name')
    description = forms.CharField(label='Details Of Service',max_length=30, required=True)
    price = forms.DecimalField(label='Price ($)',max_digits=10, required=True)
    available = forms.BooleanField(label='Show Service')
    class Meta:
        model = Services
        fields = ('name','description','price','available')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']