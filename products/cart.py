from decimal import Decimal
from django.conf import settings
from .models import Product, addOnProducts

class ProductCart(object):
    def add(self, product, addon_list, dropdown_list, quantity=1, override_quantity=False):
        product_id = str(product.id)
        addon_and_dropdown = [addon_list, dropdown_list]
        # print(addon_and_dropdown)
        
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 
                                   'price':str(product.price),
                                   'addon':[addon_and_dropdown]}
        else:
            if (addon_and_dropdown in self.cart[product_id]['addon']):
                self.cart[product_id]['quantity'] = self.cart[product_id]['quantity']
            else:
                self.cart[product_id]['quantity'] = self.cart[product_id]['quantity']
                self.cart[product_id]['addon'].append(addon_and_dropdown)
        for keyd in self.cart.keys():
            for addon in self.cart[keyd]['addon']:
                print(addon[1])
            print()
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        # self.save()

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
        for item in cart.values():
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