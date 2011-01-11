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

class StockItemAttributeValueInline(admin.TabularInline):
    model = StockItemAttributeValue

    
class ProductStockInline(admin.TabularInline):
    model = ProductStock
    extra = 0
                
class StockItemAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'package_count', 'price_override',)
    inlines = [
        StockItemAttributeValueInline,
    ]
    class Meta:
        model = StockItem

class StockItemInline(admin.StackedInline):
    model = StockItem

class ProductRelationshipInline(admin.TabularInline):
    model = ProductRelationship
    fk_name = 'from_product'

class ProductStockAdmin(admin.ModelAdmin):
    class Meta:
        model = ProductStock


class ProductAdmin(admin.ModelAdmin):
    list_display = (
         'title', 'category', 'brand',
    )
    inlines = [
        ProductStockInline,
        ProductRelationshipInline,
    ]   
    class Meta:
        model = Product
  

class ProductGalleryAdmin(admin.ModelAdmin):
    class Meta:
        model = ProductGallery


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'caption')
    class Meta:
        model = ProductImage

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

class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'help_text',)
    prepopulated_fields = {"slug": ("name",)}
    class Meta:
        model = ProductAttribute



admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductGallery, ProductGalleryAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(PriceHistory, PriceHistoryAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(StockItem, StockItemAdmin)
admin.site.register(ProductStock, ProductStockAdmin)