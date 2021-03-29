from decimal import Decimal
from django.conf import settings
from .models import Product, addOnProducts

class ProductCart(object):
    def __init__(self, request):
        # Inititialize the cart
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart