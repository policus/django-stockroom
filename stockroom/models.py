from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from datetime import datetime
from managers import CategoryChildrenManager, ActiveInventoryManager
from units import STOCKROOM_UNITS

# Set default values
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
    logo = models.ImageField(upload_to='stockroom/brand_logos', null=True, blank=True)
    
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
    image = models.ForeignKey('StockItemImage', null=True, blank=True)
    
    def __unicode__(self):
        return _(self.title)      
    
    def add_image(self, stock_item_image, *args, **kwargs):
        self.image = stock_item_image
        super(Product, self).save(*args, **kwargs)

class ProductCategory(models.Model):
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    objects = models.Manager()
    children = CategoryChildrenManager()
    
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
        return ':'
        
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
    
    class Meta:
        verbose_name = 'product relationship'
        verbose_name_plural = 'product relationships'
        
class StockItemImage(models.Model):
    stock_item = models.ForeignKey('StockItem', related_name='images')
    image = models.ImageField(upload_to='stockroom/stock_items/%Y/%m/%d')
    caption = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'
    
    def __unicode__(self):
        return _('Image for %s' % (self.stock_item,))
    
    def save(self, *args, **kwargs):
        self.stock_item.image_added()
        super(StockItemImage, self).save(*args, **kwargs)
        if self.stock_item.product.image == None:
            self.stock_item.product.add_image(self)
        
    def delete(self, *args, **kwargs):
        self.stock_item.image_removed()
        super(StockItemImage, self).delete(*args, **kwargs)


class StockItemAttribute(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    help_text = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'attribute'
        verbose_name_plural = 'attributes'

    def __unicode__(self):
        return _(self.name)

class StockItemAttributeValue(models.Model):
    attribute = models.ForeignKey('StockItemAttribute')
    value = models.CharField(max_length=255)
    unit = models.CharField(max_length=8, choices=ATTRIBUTE_VALUE_UNITS, null=True, blank=True)
    
    class Meta:
        verbose_name = 'attribute value'
        verbose_name_plural = 'attribute values'

    def __unicode__(self):
        return "%s : %s %s" % (self.attribute, self.value, self.unit)

    def display_value(self):
        return "%s %s" % (self.value, self.unit)
        
class StockItem(models.Model):
    product = models.ForeignKey('Product')
    attributes = models.ManyToManyField('StockItemAttributeValue', blank=True, null=True)
    package_title = models.CharField(max_length=60, blank=True, null=True, help_text='(ex. 3-pack of T-shirts)', default='Individual Item')
    package_count = models.IntegerField(default=1)
    inventory = models.IntegerField(default=0)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text='All prices in USD',
    )
    on_sale = models.BooleanField(default=False)
    image_count = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'inventory'
        verbose_name_plural = 'inventory'
    
    def __unicode__(self):
        return _("%s of %s" % (self.package_title, self.product))
        
    def save(self, *args, **kw):
       if self.pk is not None:
           original = StockItem.objects.get(pk=self.pk)
           if original.price != self.price:
               PriceHistory.objects.create(
                   stock_item=self,
                   price=self.price,
                   on_sale=self.on_sale,
               )
       super(StockItem, self).save(*args, **kw)
    
    def image_added(self, *args, **kwargs):
        self.image_count = self.image_count + 1
        super(StockItem, self).save(*args, **kwargs)
        return self.image_count
    
    def image_removed(self, *args, **kwargs):
        self.image_count = self.image_count - 1
        super(StockItem, self).save(*args, **kwargs)
        return self.image_count
       
class PriceHistory(models.Model):
    stock_item = models.ForeignKey('StockItem')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='All prices in USD')
    on_sale = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_on']
        verbose_name = 'price history'
        verbose_name_plural = 'price history'
    
    def __unicode__(self):
        return self.price
        
class Cart(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    checked_out = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'
    
    def __unicode__(self):
        cart_time = datetime.strftime(self.created_on, "%b %d, %Y at %I:%M:%S%p")
        return _("Cart created on %s" % cart_time)

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', related_name='cart_items')
    stock_item = models.ForeignKey('StockItem')
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        verbose_name = 'item in cart'
        verbose_name_plural = 'items in carts'
        ordering = ('cart',)
    
    def __unicode__(self):
        return _("%s" % (self.stock_item))
    
    def subtotal(self):
        return self.quantity * self.stock_item.get_price()