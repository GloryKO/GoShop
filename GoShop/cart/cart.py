from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:
    def __init__(self,request):
        self.session = request.session #gets the current session 
        cart = self.session.get(settings.CART_SESSION_ID) # get the cart from the session if there exist a cart already.
        if not cart :
            #set a new cart in the session (a dictionary of product ids with prices and quantity)
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self,product,quantity,override_quantity=False):
                """
                Add a product to the cart or update its quantity.
                """
                product_id =str(product.id)
                if product_id not in self.cart: #check if product does not already exists in the cart 
                    self.cart[product_id] = {'quantity': 0,'price': str(product.price)}
                if override_quantity:
                    self.cart[product_id]['quantity'] = quantity
                else:
                    self.cart[product_id]['quantity'] += quantity
                self.save()
    
    def save(self):
        self.session.modified = True
    
    def remove(self,product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids) #get the product ids and add them to the cart
        cart = self.cart.copy()
