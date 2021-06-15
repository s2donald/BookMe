from decimal import Decimal
from django.conf import settings
from .models import Product, MainProductDropDown, ProductDropDown, Coupon
import decimal
class ProductCart(object):
    def add(self, product, dropdown_list,dropdown_addon, quantity=1, override_quantity=False):
        product_id = str(product.id)
        price = decimal.Decimal(0)
        for dropd in dropdown_addon:
            price += dropd.price
        price += product.price
        self.cart.clear()
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 
                                   'price':str(price),
                                   'dropdown':dropdown_list}
        else:
            self.cart[product_id]['dropdown'] = dropdown_list
            self.cart[product_id]['price'] = str(price)
            # if (addon_and_dropdown in self.cart[product_id]['addon']):
            #     self.cart[product_id]['quantity'] = self.cart[product_id]['quantity']
            #     # self.cart[product_id]['addon'][addon_and_dropdown][1]+=1
            # else:
            #     self.cart[product_id]['quantity'] = self.cart[product_id]['quantity']
            #     self.cart[product_id]['addon'].append(addon_and_dropdown)
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
            cart[str(product.id)]['company'] = product.business

        for item in cart.values():
            item['dropdownoptions'] = ProductDropDown.objects.filter(id__in=item['dropdown'])
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
    
    def save(self):
        self.session.modified = True

    def __init__(self, request):
        # Inititialize the cart
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')
    
    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None
    
    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)
    
    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
