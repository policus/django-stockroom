from tastypie import resources
from models import ProductCategory, CartItem
from django.http import HttpRequest

class ProductCategoryResource(resources.ModelResource):
    
    class Meta:
        queryset = ProductCategory.objects.filter(active=True)
        resource_name = 'categories'
    
class CartResource(resources.Resource):
    def obj_get_list(self, filters=None, *args, **kwargs):
        
        cart_items = CartItem.objects.filter(cart=request.cart) 
        return cart_items
    
    class Meta:
        object_class = CartItem
        resource_name = 'cart'