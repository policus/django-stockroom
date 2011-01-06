from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from datetime import datetime
from managers import CategoryChildrenManager, ActiveInventoryManager
from thumbs import ImageWithThumbsField
from units import STOCKROOM_UNITS

# Set default values
    
IMAGE_GALLERY_LIMIT = getattr(settings, 'IMAGE_GALLERY_LIMIT', 8)
STOCKROOM_CATEGORY_SEPARATOR = getattr(settings, 'STOCKROOM_CATEGORY_SEPARATOR', ' :: ')
PRODUCT_THUMBNAILS = getattr(settings, 'STOCKROOM_PRODUCT_THUMBNAIL_SIZES', None)
ATTRIBUTE_VALUE_UNITS = getattr(settings, 'STOCKROOM_UNITS', STOCKROOM_UNITS)

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
    relationships = models.ManyToManyField('self', through='ProductRelationship', symmetrical=False, related_name='related_to')    
    created_on = models.DateTimeField(auto_now_add=True)
    last_updates = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return _(self.title)
    
    def get_price(self):
        try:
            price = Price.objects.filter(product=self).order_by('-created_on')[0]
            return price.price
        except Price.DoesNotExist:
            return None
    
    def get_thumb(self):
        try:
            gallery = ProductGallery.objects.filter(product=self)[0]
            thumb = gallery.get_thumbnails()
            return thumb[0].image
        except ProductGallery.DoesNotExist:
            return False        

class ProductAttribute(models.Model):
    name = models.CharField(max_length=80)
    help_text = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        return _(self.name)

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
        # we need to encode this to ascii as per python docs:
        # http://docs.python.org/reference/datamodel.html#object.__repr__
        return self.get_separator().join(parent_list).encode("ascii", "replace")

    def save(self, force_insert=False, force_update=False):
        self.slug = slugify(self.name)
        super(ProductCategory, self).save()
                

class ProductRelationship(models.Model):
    from_product = models.ForeignKey('Product', related_name='related_products')
    to_product = models.ForeignKey('Product', related_name='to_product')
    description = models.CharField(max_length=140, help_text="A tweet-length (140 character) description of the relationship")
    
    def __unicode__(self):
        return _('Product related to %s' % self.from_product)
        

class ProductGallery(models.Model):
    product = models.ForeignKey('Product', related_name='gallery')
    images_available = models.IntegerField(default=IMAGE_GALLERY_LIMIT)
    
    class Meta:
        verbose_name_plural = 'image galleries'
    
    def __unicode__(self):
        return_string = _("Image gallery for %s" % self.product)
        return return_string
    
    def image_added(self):
        self.images_available = self.images_available - 1
        super(ProductGallery, self).save()
    
    def get_thumbnails(self):
        thumbnails = []
        for i in self.images.all():
            thumbnails.append(i)
        return thumbnails
        
class ProductImage(models.Model):
    gallery = models.ForeignKey('ProductGallery', related_name='images')
    image = ImageWithThumbsField(upload_to='stockroom/product_images/%Y/%m/%d', sizes=PRODUCT_THUMBNAILS)
    caption = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'images'
    
    def __unicode__(self):
        return_string = _("%s" % self.gallery.product)
        return return_string
    
    def save(self, force_insert=False, force_update=False):
        self.gallery.image_added()
        super(ProductImage, self).save()
    
class StockItem(models.Model):
    product = models.ForeignKey('Product', related_name='stock')
    package_title = models.CharField(max_length=60, blank=True, null=True, help_text='(ex. 3-pack of T-shirts)')
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
        return_string = "%s %s" % (self.product, self.package_title)
        if self.package_count > 1:
            return_string += "%s-pack " % self.package_count
        return return_string
    
    def get_price(self):
        if self.price:
            return self.price
        else:
            return self.product.get_price()

class StockItemAttribute(models.Model):
    stock_item = models.ForeignKey('StockItem', related_name='stock_attributes')
    product_attribute = models.ForeignKey('ProductAttribute')
    value = models.CharField(max_length=255)
    unit = models.CharField(max_length=8, choices=ATTRIBUTE_VALUE_UNITS)
    
    def __unicode__(self):
        return "%s, %s" % (self.stock_item, self.product_attribute)
        
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
    
    def subtotal(self):
        return self.quantity * self.stock_item.get_price()