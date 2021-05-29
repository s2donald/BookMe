from decimal import Decimal
from django.conf import settings
# from .models import Product, MainProductDropDown, ProductDropDown
from cities.models import City, Region
import decimal
class RegionCountrySession(object):
    def add(self, country_code, region_list):
        if country_code not in self.region:
            self.region[country_code] = {'region_list': region_list}
        else:
            self.region[country_code]['region_list'] = region_list
        self.save()

    def clear(self):
        del self.session[settings.REGION_SESSION_ID]
        self.save()
    
    def save(self):
        self.session.modified = True

    def __iter__(self):
        country_code = self.region.keys()
        region = self.region.copy()
        for country in country_code:
            region[str(country)]['country'] = country
        for item in region.values():
            # print(item)
            item['regions'] = Region.objects.filter(country__code=item)
            yield item

    def __init__(self, request):
        # Inititialize the cart
        self.session = request.session
        region = self.session.get(settings.REGION_SESSION_ID)
        if not region:
            region = self.session[settings.REGION_SESSION_ID] = {}
        self.region = region