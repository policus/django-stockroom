from django.conf.urls.defaults import *
from piston.resource import Resource

from handlers import ProductCategoryHandler, ProductHandler, StockHandler, InventoryHandler, CartHandler, ProductGalleryHandler

category_handler = Resource(ProductCategoryHandler)
product_handler = Resource(ProductHandler)
product_gallery_handler = Resource(ProductGalleryHandler)
stock_handler = Resource(StockHandler)
inventory_handler = Resource(InventoryHandler)
cart_handler = Resource(CartHandler)

urlpatterns = patterns('',
    url(r'^categories/$', category_handler),
    url(r'^categories/(?P<slug>[-\w]+)/$', category_handler),
    url(r'^products/$', product_handler),
    url(r'^products/(?P<product_pk>\d+)/$', product_handler),
    url(r'^products/(?P<product_pk>\d+)/$', product_gallery_handler),
    url(r'^products/(?P<product_pk>\d+)/inventory/$', inventory_handler),
    url(r'^cart/$', cart_handler),
    url(r'^cart/(?P<pk>\d+)/$', cart_handler),
)