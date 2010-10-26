import datetime
from models import Cart as CartModel, CartItem
CART_ID = 'CART-ID'

class ItemAlreadyExists(Exception):
    pass

class ItemDoesNotExist(Exception):
    pass

class Cart(object):
    def __init__(self, request):
        cart_id = request.session.get(CART_ID)
        if cart_id:
            try:
                cart = CartModel.objects.get(id=cart_id, checked_out=False)
            except CartModel.DoesNotExist:
                cart = self.new(request)
        else:
            cart = self.new(request)
        self.cart = cart
        
    def __iter__(self):
        for item in self.cart.item_set.all():
            yield item
    
    def new(self, request):
        cart = CartModel()
        cart.save()
        request.session[CART_ID] = cart.id
        return cart
    
    def add(self, product, unit_price, quantity=1):
        try:
            cart_item = CartItem.objects.get(cart=self.cart, product=product)
        except models.CartItem.DoesNotExist:
            cart_item = models.CartItem()
            cart_item.cart = self.cart
            cart_item.product = product
            cart_item.unit_price = unit_price
            cart_item.quantity = quantity
            cart_item.save()
        else:
            raise ItemAlreadyExists
    
    def remove(self, item):
        try:
            cart_item = CartItem.objects.get(pk=item.pk)
        except CartItem.DoesNotExist:
            raise ItemDoesNotExist
        else:
            cart_item.delete()
    
    def update(self, product, unit_price, quantity):
        try:
            cart_item = models.CartItem.objects.get(cart=self.cart, product=product)
            cart_item.cart = self.cart
            cart_item.product = product
            cart_item.unit_price = unit_price
            cart_item.quantity = quantity
            cart_item.save(force_update=True)
        except models.CartItem.DoesNotExist:
            raise ItemDoesNotExist
    
    def clear(self):
        for cart_item in self.cart.item_set.all():
            cart_item.delete()
    
    def get_quantity(self, product):
        try:
            cart_item = CartItem.objects.get(cart=self.cart, product=product)
            return cart_item.quantity
        
        except models.CartItem.DoesNotExist:
            return 0
    
    def total_quantity(self):
        cart_quantity = 0
        try:
            cart_items = CartItem.objects.filter(cart=self.cart)
        except CartItem.DoesNotExist:
            return cart_quantity
        
        for item in cart_items:
            cart_quantity = cart_quantity + item.quantity
        
        return cart_quantity
    
    def checkout_cart(self):
        self.cart.checked_out = True
        self.cart.save()
        return True
    