from decimal import Decimal
from django.conf import settings
from .models import Pizza


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1.0, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0.0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Pizza.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * Decimal(item['quantity'])
            yield item

    def __len__(self):
        return 1 + int(sum(item['quantity'] for item in self.cart.values()))

    def get_total_price(self):
        return sum(Decimal(item['price']) * Decimal(item['quantity']) for item in self.cart.values())

    def valid_cart(self):
        return (2 * sum(item['quantity'] for item in self.cart.values()) % 2) == 0

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True