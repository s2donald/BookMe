from django import forms
from .models import Order
from django_countries.widgets import CountrySelectWidget
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]
from cities.models import City, Region
from django_countries.fields import CountryField

class OrderCreateForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name',max_length=50, required=True)
    last_name = forms.CharField(label='Last Name',max_length=50, required=True)
    phone = forms.CharField(label='Phone Number',required=True, max_length=17)
    email = forms.EmailField(label='Email',required=True)
    address = forms.CharField(required=True, max_length=200)
    country = CountryField().formfield()

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'country', 'postal_code', 'city', 'state']
        widgets = {'country': CountrySelectWidget()}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            # self.fields['state'].queryset = Region.objects.filter(country__code='CA').order_by('name')
            self.fields['state'].queryset = Region.objects.none()
        except AttributeError:
            pass

        if 'country' in self.data:
            try:
                country_code = self.data.get('country')
                self.fields['state'].queryset = Region.objects.filter(country__code=country_code)
            except (ValueError, TypeError):
                pass