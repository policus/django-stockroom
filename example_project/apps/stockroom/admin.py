from django.contrib import admin
from models import *

class ProductCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'parent',]
    class Meta:
        model = ProductCategory


class ManufacturerAdmin(admin.ModelAdmin):
    class Meta:
        model = Manufacturer


class BrandAdmin(admin.ModelAdmin):
    class Meta:
        model = Brand


class PriceInline(admin.TabularInline):
    model = Price
    extra = 1
    fields = ('price', 'on_sale',)


class MeasurementUnitAdmin(admin.ModelAdmin):
    class Meta:
        model = MeasurementUnit


class MeasurementAdmin(admin.ModelAdmin):
    class Meta:
        model = Measurement


class StockItemAdmin(admin.ModelAdmin):
    class Meta:
        model = StockItem


class StockItemInline(admin.TabularInline):
    model = StockItem
    fk_name = 'product'
    extra = 1


class InventoryAdmin(admin.ModelAdmin):
    class Meta:
        model = Inventory


class InventoryInline(admin.TabularInline):
    model = Inventory

class ColorAdmin(admin.ModelAdmin):
    class Meta:
        model = Color


class ProductRelationshipInline(admin.TabularInline):
    model = ProductRelationship
    fk_name = 'from_product'


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductRelationshipInline,        
    ]
    list_display = (
         'title', 'category', 'brand',
    )
    class Meta:
        model = Product

class ProductGalleryAdmin(admin.ModelAdmin):
    class Meta:
        model = ProductGallery


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'caption')
    class Meta:
        model = ProductImage


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
admin.site.register(Product, ProductAdmin)
admin.site.register(MeasurementUnit, MeasurementUnitAdmin)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(StockItem, StockItemAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(ProductGallery, ProductGalleryAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)