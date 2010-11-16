from datetime import datetime
from cart import Cart
import logging

class StockroomMiddleware(object):
    def process_request(self, request):
        if not hasattr(request, 'cart'):
            cart = Cart(request)
            request.cart = cart
        