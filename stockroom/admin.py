from django.contrib import admin
from django.db import models
from django import forms
from django.forms.models import inlineformset_factory

from models import *

class ProductCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'parent',]
    list_filter = ('parent',)
    class Meta:
        model = ProductCategory


class ManufacturerAdmin(admin.ModelAdmin):
    class Meta:
        model = Manufacturer


class BrandAdmin(admin.ModelAdmin):
    class Meta:
        model = Brand

class StockItemInline(admin.StackedInline):
    model = StockItem
    extra = 0
    filter_horizontal = ('attributes',)

class StockItemImageAdmin(admin.ModelAdmin):
    class Meta:
        model = StockItemImage

class StockItemImageInline(admin.TabularInline):
    model = StockItemImage
    extra = 1
    
class StockItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'inventory', 'image_count')
    filter_horizontal = ('attributes',)
    inlines = [
        StockItemImageInline,
    ]
    class Meta:
        model = StockItem

class StockItemAttributeAdmin(admin.ModelAdmin):
    class Meta:
        model = StockItemAttribute

class StockItemAttributeValueAdmin(admin.ModelAdmin):
    class Meta:
        model = StockItemAttributeValue


class ProductRelationshipInline(admin.TabularInline):
    model = ProductRelationship
    fk_name = 'from_product'

class ProductAdmin(admin.ModelAdmin):
    inlines = [
        StockItemInline,
        ProductRelationshipInline,
    ]
    list_display = ('title', 'category', 'brand',)
    class Meta:
        model = Product

class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'price')
    class Meta:
        model = PriceHistory

class CartAdmin(admin.ModelAdmin):
    class Meta:
        model = Cart

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('stock_item', 'quantity', 'cart')
    class Meta:
        model = CartItem


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(PriceHistory, PriceHistoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(StockItem, StockItemAdmin)
admin.site.register(StockItemAttribute, StockItemAttributeAdmin)
admin.site.register(StockItemAttributeValue, StockItemAttributeValueAdmin)
admin.site.register(StockItemImage, StockItemImageAdmin)