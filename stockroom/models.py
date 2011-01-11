from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from datetime import datetime
from managers import CategoryChildrenManager, ActiveInventoryManager
from thumbs import ImageWithThumbsField
from units import STOCKROOM_UNITS

# Set default values
    
IMAGE_GALLERY_LIMIT = getattr(settings, 'STOCKROOM_IMAGE_GALLERY_LIMIT', 8)
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
        return _(self.name)
    
class Product(models.Model):
    category = models.ForeignKey('ProductCategory', null=True, blank=True)
    brand = models.ForeignKey('Brand')
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    sku = models.CharField(max_length=30, null=True, blank=True, help_text='An internal unique identifier for this product')
    relationships = models.ManyToManyField('self', through='ProductRelationship', symmetrical=False, related_name='related_to')    
    created_on = models.DateTimeField(auto_now_add=True)
    last_updates = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='All prices in USD')
    on_sale = models.BooleanField(default=False)

    def __unicode__(self):
        return _(self.title)

    def save(self, *args, **kw):
        if self.pk is not None:
            original = Product.objects.get(pk=self.pk)
            if original.price != self.price:
                PriceHistory.objects.create(
                    product=self,
                    price=self.price,
                    on_sale=self.on_sale,
                )
        super(Product, self).save(*args, **kw)      

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

class ProductStock(models.Model):
    for_sale = models.BooleanField(default=True)
    product = models.ForeignKey('Product')
    stock_item = models.ForeignKey('StockItem')
    inventory = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    disable_sale_at = models.IntegerField(default=0, blank=True, null=True, help_text='Stockroom will stop the item from being sold once this quantity is reached (will accept negative numbers). Leave blank to disable')
    order_throttle = models.IntegerField(blank=True, null=True, help_text='The maximum amount of this item that can be in an individaul order')
    
class ProductAttribute(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    help_text = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return _(self.name)

class StockItemAttributeValue(models.Model):
    stock_item = models.ForeignKey('StockItem', related_name='attribute_values')
    product_attribute = models.ForeignKey('ProductAttribute')
    value = models.CharField(max_length=255)
    unit = models.CharField(max_length=8, choices=ATTRIBUTE_VALUE_UNITS, null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.value, self.unit)

    def display_value(self):
        return "%s %s" % (self.value, self.unit)
        
class StockItem(models.Model):
    package_title = models.CharField(max_length=60, blank=True, null=True, help_text='(ex. 3-pack of T-shirts)', default='Individual Item')
    package_count = models.IntegerField(default=1)
    price_override = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text='All prices in USD. Use this field to override the standard pricing of a product for this sepcific stock item.',
        blank=True,
        null=True,
    )
    
    def __unicode__(self):
        if self.package_title:
            package_title = _(self.package_title)
        else:
            package_title = None
        
        attributes = StockItemAttributeValue.objects.filter(stock_item=self)
        if package_title:
            attribute_string = '%s - ' % (package_title,)
        else:
            attribute_string = ''
                
        for a in attributes:
            attribute_string += "/%s:%s" % (a.product_attribute, a.display_value())
            
        return attribute_string
        
    def get_price(self):
        if self.price_override:
            return self.price_override
        else:
            return self.product.price
        
class PriceHistory(models.Model):
    product = models.ForeignKey('Product', related_name='pricing')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='All prices in USD')
    on_sale = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_on']
    
    def __unicode__(self):
        return _("Pricing for %s" % (self.product.title))

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