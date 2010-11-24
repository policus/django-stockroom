from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _

try:
    from taggit.managers import TaggableManager
except ImportError:
    raise "You must have django-taggit installed to use django-stockroom"

from datetime import datetime

from managers import CategoryChildrenManager, ActiveInventoryManager
from thumbs import ImageWithThumbsField

# Set default values
    
if settings.IMAGE_GALLERY_LIMIT:
    IMAGE_GALLERY_LIMIT = settings.IMAGE_GALLERY_LIMIT
else:
    IMAGE_GALLERY_LIMIT = 8

if settings.STOCKROOM_CATEGORY_SEPARATOR:
    STOCKROOM_CATEGORY_SEPARATOR = settings.STOCKROOM_CATEGORY_SEPARATOR
else:
    STOCKROOM_CATEGORY_SEPARATOR = ' :: '
    
if settings.STOCKROOM_PRODUCT_THUMBNAIL_SIZES:
    PRODUCT_THUMBNAILS = settings.STOCKROOM_PRODUCT_THUMBNAIL_SIZES
else:
    PRODUCT_THUMBNAILS = None

class Manufacturer(models.Model):
    name = models.CharField(max_length=120)
    website = models.URLField(verify_exists=True, null=True, blank=True)
    
    def __unicode__(self):
        return _(self.name)


class Brand(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    manufacturer = models.ForeignKey('Manufacturer')
    logo = ImageWithThumbsField(upload_to='stockroom/brand_logos', null=True, blank=True)
    
    def __unicode__(self):
        return _("%s - %s" % (self.manufacturer, self.name))
    

class Product(models.Model):
    category = models.ForeignKey('ProductCategory', null=True, blank=True)
    brand = models.ForeignKey('Brand')
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    sku = models.CharField(max_length=30, null=True, blank=True, help_text='An internal unique identifier for this product')
    tags = TaggableManager()
    relationships = models.ManyToManyField('self', through='ProductRelationship', symmetrical=False, related_name='related_to')    
    created_on = models.DateTimeField(auto_now_add=True)
    last_updates = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return _(self.title)
    
    def get_price(self):
        try:
            price = Price.objects.filter(product=self).order_by('-created_on')[:1]
        except Price.DoesNotExist:
            price = None
        return "$%s" % (price[0].price,)

class ProductCategory(models.Model):
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return _(self.name)

    def _recurse_for_parents(self, category_object):
        parent_list = []
        if category_object.parent_id:
            parent = category_object.parent
            parent_list.append(parent.name)
            more = self._recurse_for_parents(parent)
            parent_list.extend(more)

        if category_object == self and parent_list:
            parent_list.reverse()

        return parent_list

    def get_separator(self):
        return STOCKROOM_CATEGORY_SEPARATOR
        
    def _parents_repr(self):
        parent_list = self._recurse_for_parents(self)
        return self.get_separator().join(parent_list)

    def _pre_save(self):
        parent_list = self._recurse_for_parents(self)
        if self.name in parent_list:
            raise "You can't save a category in itself"

    def __repr__(self):
        parent_list = self._recurse_for_parents(self)
        parent_list.append(self.name)
        return self.get_separator().join(parent_list)

    def save(self, force_insert=False, force_update=False):
        self.slug = slugify(self.name)
        super(ProductCategory, self).save()
                

class ProductRelationship(models.Model):
    from_product = models.ForeignKey('Product', related_name='from_product')
    to_product = models.ForeignKey('Product', related_name='to_product')
    description = models.CharField(max_length=140, help_text="A tweet-length (140 character) description of the relationship")
    
    def __unicode__(self):
        return _('Product related to %s' % self.from_product)
        

class ProductGallery(models.Model):
    product = models.ForeignKey('Product', related_name='gallery')
    images_available = models.IntegerField(default=IMAGE_GALLERY_LIMIT)
    color = models.ForeignKey('Color', null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'image galleries'
    
    def __unicode__(self):
        return_string = _("Image gallery for %s" % self.product)
        if self.color:
            return_string += _(" in %s" % self.color)
        return return_string
    
    def image_added(self):
        self.images_available = self.images_available - 1
        super(ProductGallery, self).save()
    

class ProductImage(models.Model):
    gallery = models.ForeignKey('ProductGallery', related_name='image')
    image = ImageWithThumbsField(upload_to='stockroom/product_images/%Y/%m/%d', sizes=PRODUCT_THUMBNAILS)
    caption = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'images'
    
    def __unicode__(self):
        return_string = _("%s" % self.gallery.product)
        if self.gallery.color:
            return_string += _(" in %s" % self.gallery.color)
        return return_string
    
    def save(self, force_insert=False, force_update=False):
        self.gallery.image_added()
        super(ProductImage, self).save()
            

class MeasurementUnit(models.Model):
    name = models.CharField(max_length=20)
    abbreviation = models.CharField(max_length=8, blank=True, null=True)
    verbose_name_plural = models.CharField(max_length=10, blank=True, null=True)
    
    def __unicode__(self):
        if self.abbreviation:
            return _(self.abbreviation)
        else:
            return _(self.name)
        

class Measurement(models.Model):
    measurement = models.CharField(max_length=8)
    unit = models.ForeignKey('MeasurementUnit')
    
    def __unicode__(self):
        return _('%s - %s' % (self.unit, self.measurement))


class Color(models.Model):
    name = models.CharField(max_length=30)
    red = models.IntegerField(default=0, blank=True, null=True)
    blue = models.IntegerField(default=0, blank=True, null=True)
    green = models.IntegerField(default=0, blank=True, null=True)
    swatch = ImageWithThumbsField(upload_to='stockroom/color_swatches/', blank=True, null=True)
    
    def __unicode__(self):
        return _(self.name)
    

class StockItem(models.Model):
    product = models.ForeignKey('Product', related_name='stock')
    measurement = models.ForeignKey('Measurement', blank=True, null=True)
    color = models.ForeignKey('Color', blank=True, null=True)
    package_count = models.IntegerField(default=1)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text='All prices in USD. Use this field to override the standard pricing of a product for this sepcific stock item.',
        blank=True,
        null=True,
        verbose_name='Override Product Pricing'
    )
     
    def __unicode__(self):
        return_string = ''
        if self.package_count > 1:
            return_string += "%s-pack " % self.package_count
        return_string += "%s of %s" % (self.measurement, self.product)
        if self.color:
            return_string += " in %s" % self.color
        return return_string
        
class Price(models.Model):
    product = models.ForeignKey('Product', related_name='pricing')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='All prices in USD')
    on_sale = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_on']
    
    def __unicode__(self):
        return _("Pricing for %s" % (self.product.title))


class Inventory(models.Model):
    stock_item = models.ForeignKey('StockItem')
    for_sale = models.BooleanField(default=True)
    quantity = models.IntegerField(default=0)
    disable_sale_at = models.IntegerField(default=0, blank=True, null=True, help_text='Stockroom will stop the item from being sold once this quantity is reached (will accept negative numbers). Leave blank to disable')
    order_throttle = models.IntegerField(blank=True, null=True, help_text='The maximum amount of this item that can be in an individaul order')
    active = ActiveInventoryManager()
    
    class Meta:
        verbose_name_plural = 'inventory'
    
    def __unicode__(self):
        return _("%s" % (self.stock_item,))
    

class Cart(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    checked_out = models.BooleanField(default=False)
    
    def __unicode__(self):
        cart_time = datetime.strftime(self.created_on, "%b %d, %Y at %I:%M:%S%p")
        return _("Cart created on %s" % cart_time)


class CartItem(models.Model):
    cart = models.ForeignKey('Cart', related_name='cart_items')
    stock_item = models.ForeignKey('StockItem')
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        verbose_name = _('cart item')
        verbose_name_plural = _('cart items')
        ordering = ('cart',)
    
    def __unicode__(self):
        return _("%s" % (self.stock_item))
    
    def sub_total(self):
        return self.quantity * self.unit_price