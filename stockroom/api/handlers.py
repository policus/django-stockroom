from django.db.models import Count
from django.http import HttpResponse
from piston.handler import BaseHandler
from piston.utils import validate, rc
from stockroom.models import ProductCategory, Product, Inventory, StockItem, Color, CartItem, Cart as CartModel
from stockroom.cart import Cart
from stockroom.forms import CartItemForm

import logging

class CsrfExemptBaseHandler(BaseHandler):
    """
        handles request that have had csrfmiddlewaretoken inserted 
        automatically by django's CsrfViewMiddleware
        see: http://andrew.io/weblog/2010/01/django-piston-and-handling-csrf-tokens/
    """
    def flatten_dict(self, dct):
        if 'csrfmiddlewaretoken' in dct:
            dct = dct.copy()
            del dct['csrfmiddlewaretoken']
        return super(CsrfExemptBaseHandler, self).flatten_dict(dct)
            
class ProductCategoryHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = ProductCategory
    
    def read(self, request, slug=None):
        if slug:
            try:
                category = ProductCategory.objects.select_related().get(active=True, slug=slug)
                children = []
                for child in category.children.all():
                    logging.debug(child)
                    children.append({child.slug : child})
                response = {'details' : category, 'children' : children, }
                
            except ProductCategory.DoesNotExist:
                response = None
            return response
            
        else:
            try:
                categories = ProductCategory.objects.filter(active=True, parent=None)
            except ProductCategory.DoesNotExist:
                categories = None
            return categories

class ProductHandler(BaseHandler):
    allowed_methods = ('GET',)
    exclude = (),
    model = Product
    
    def read(self, request, pk=None):
        if pk:
            try:
                product = Product.objects.select_related().get(pk=pk)   
                stock = StockItem.objects.filter(product=product)
                colors = []
                for s in stock:
                    colors.append(s.color)
                response = {
                    'product' : product,
                    'stock' : stock,
                    'colors' : colors,
                }
            except Product.DoesNotExist:
                response = None
            return response
            
        else: 
            try:
                products = Product.objects.select_related().all()
                response = []
                for p in products:
                    item = {
                        'id' : p.pk,
                        'title' : p.title,
                        'description' : p.description,
                        'sku' : p.sku,
                        'tags' : p.tags.all(),
                        'category' : {
                            'id' : p.category.pk,
                            'name' : p.category.name,
                            'slug' : p.category.slug,
                        },
                        'brand' : {
                            'id' : p.brand.pk,
                            'name' : p.brand.name,
                            'manufacturer' : {
                                'id' : p.brand.manufacturer.pk,
                                'name' : p.brand.manufacturer.name,
                            },
                        },
                    }
                    
                    inventory = []
                    for s in p.stock.all():
                        inventory.append(s)
                        
                    
                    
            except Product.DoesNotExist:
                response = None
            return response

class StockHandler(BaseHandler):
    allwed_methods = ('GET',)
    exclude = ()
    model = StockItem
    
    def read(self, request, pk=None):
        if pk:
            try:
                stock = StockItem.objects.select_related().filter(product=pk)
            except StockItem.DoesNotExist:
                stock = None
            return stock

class InventoryHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Inventory
    
    def read(self, request, pk=None):
        try:
            inventory = Inventory.active.filter(stock_item__product=pk)
            stock = []
            for s in inventory:
                stock.append({
                    'id' : s.pk,
                    'title' : s.__unicode__(),
                    'color' : s.stock_item.color,
                    'measurement' : {
                        'value' : s.stock_item.measurement.measurement,
                        'unit' : s.stock_item.measurement.unit,
                    },
                    'package_count' : s.stock_item.package_count,
                    'quantity' : s.quantity,
                    'order_throttle': s.order_throttle,
                    'disable_sale_at': s.disable_sale_at,
                })
                
        except Inventory.DoesNotExist:
            stock = None
        
        return stock

class CartHandler(CsrfExemptBaseHandler):
    allowed_methods = ('GET', 'PUT',)
    exclude = (),
    model = CartItem
        
    def read(self, request, pk=None):
        cart = Cart(request)
        cart_info = cart.summary()
    
        if pk:
            try:
                cart_item = CartItem.objects.get(pk=pk, cart=cart_info.pk)
            except CartItem.DoesNotExist:
                return rc.NOT_FOUND
            
            response = {
                'pk' : cart_item.pk,
                'item' : cart_item.stock_item,
                'quantity' : cart_item.quantity,
            }
            
        else:
            cart_items = []                
            for item in cart:
                cart_items.append({
                    'product' : item.stock_item.product,
                    'package_count' : item.stock_item.package_count,
                    'color' : item.stock_item.color,
                    'measurement': item.stock_item.measurement,
                })
        
            response = {
                'checked_out' : cart_info.checked_out,
                'created_on' : cart_info.created_on,
                'items' : cart_items,
            }
            
        return response
    
    
    @validate(CartItemForm, 'PUT')
    def update(self, request):
        item = request.form.cleaned_data['stock_item']
        quantity = request.form.cleaned_data['quantity']
        cart = Cart(request)
        cart.update(item, item.get_price(), quantity)
        cart_info = cart.summary()
        cart_items = []
        for item in cart:
            cart_items.append({
                'product' : item.stock_item.product,
                'package_count' : item.stock_item.package_count,
                'quantity' : item.quantity,
                'unit_price' : item.stock_item.get_price(),
                'color' : item.stock_item.color,
                'measurement': item.stock_item.measurement,
            })

        response = {
            'checked_out' : cart_info.checked_out,
            'created_on' : cart_info.created_on,
            'items' : cart_items,
        }
        return response
