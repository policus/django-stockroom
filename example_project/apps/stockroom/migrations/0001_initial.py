# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Manufacturer'
        db.create_table('stockroom_manufacturer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('stockroom', ['Manufacturer'])

        # Adding model 'Brand'
        db.create_table('stockroom_brand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('manufacturer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stockroom.Manufacturer'])),
        ))
        db.send_create_signal('stockroom', ['Brand'])

        # Adding model 'Product'
        db.create_table('stockroom_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stockroom.ProductCategory'], null=True, blank=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stockroom.Brand'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sku', self.gf('django.db.models.fields.CharField')(max_length=30, unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('stockroom', ['Product'])

        # Adding model 'ProductCategory'
        db.create_table('stockroom_productcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, unique=True, max_length=50, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stockroom.ProductCategory'], null=True, blank=True)),
        ))
        db.send_create_signal('stockroom', ['ProductCategory'])

        # Adding model 'ProductRelationship'
        db.create_table('stockroom_productrelationship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='from_product', to=orm['stockroom.Product'])),
            ('to_product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='to_product', to=orm['stockroom.Product'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('stockroom', ['ProductRelationship'])

        # Adding model 'MeasurementUnit'
        db.create_table('stockroom_measurementunit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length=8, null=True, blank=True)),
            ('verbose_name_plural', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
        ))
        db.send_create_signal('stockroom', ['MeasurementUnit'])

        # Adding model 'Measurement'
        db.create_table('stockroom_measurement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('measurement', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stockroom.MeasurementUnit'])),
        ))
        db.send_create_signal('stockroom', ['Measurement'])

        # Adding model 'Color'
        db.create_table('stockroom_color', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('red', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('blue', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('green', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('swatch', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('stockroom', ['Color'])

        # Adding model 'StockItem'
        db.create_table('stockroom_stockitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stockroom.Product'])),
            ('measurement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stockroom.Measurement'], null=True, blank=True)),
            ('color', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stockroom.Color'], null=True, blank=True)),
            ('package_count', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('stockroom', ['StockItem'])

        # Adding model 'Price'
        db.create_table('stockroom_price', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stock_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stockroom.StockItem'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('on_sale', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('stockroom', ['Price'])

        # Adding model 'Inventory'
        db.create_table('stockroom_inventory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stock_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stockroom.StockItem'])),
            ('for_sale', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('disable_sale_at', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('order_throttle', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('stockroom', ['Inventory'])


    def backwards(self, orm):
        
        # Deleting model 'Manufacturer'
        db.delete_table('stockroom_manufacturer')

        # Deleting model 'Brand'
        db.delete_table('stockroom_brand')

        # Deleting model 'Product'
        db.delete_table('stockroom_product')

        # Deleting model 'ProductCategory'
        db.delete_table('stockroom_productcategory')

        # Deleting model 'ProductRelationship'
        db.delete_table('stockroom_productrelationship')

        # Deleting model 'MeasurementUnit'
        db.delete_table('stockroom_measurementunit')

        # Deleting model 'Measurement'
        db.delete_table('stockroom_measurement')

        # Deleting model 'Color'
        db.delete_table('stockroom_color')

        # Deleting model 'StockItem'
        db.delete_table('stockroom_stockitem')

        # Deleting model 'Price'
        db.delete_table('stockroom_price')

        # Deleting model 'Inventory'
        db.delete_table('stockroom_inventory')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'stockroom.brand': {
            'Meta': {'object_name': 'Brand'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stockroom.Manufacturer']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'stockroom.color': {
            'Meta': {'object_name': 'Color'},
            'blue': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'green': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'red': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'swatch': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'stockroom.inventory': {
            'Meta': {'object_name': 'Inventory'},
            'disable_sale_at': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'for_sale': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_throttle': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stock_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stockroom.StockItem']"})
        },
        'stockroom.manufacturer': {
            'Meta': {'object_name': 'Manufacturer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'stockroom.measurement': {
            'Meta': {'object_name': 'Measurement'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measurement': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stockroom.MeasurementUnit']"})
        },
        'stockroom.measurementunit': {
            'Meta': {'object_name': 'MeasurementUnit'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'verbose_name_plural': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'stockroom.price': {
            'Meta': {'ordering': "['-created_on']", 'object_name': 'Price'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'on_sale': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'stock_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stockroom.StockItem']"})
        },
        'stockroom.product': {
            'Meta': {'object_name': 'Product'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stockroom.Brand']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stockroom.ProductCategory']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relationships': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_to'", 'symmetrical': 'False', 'through': "orm['stockroom.ProductRelationship']", 'to': "orm['stockroom.Product']"}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'stockroom.productcategory': {
            'Meta': {'object_name': 'ProductCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stockroom.ProductCategory']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'})
        },
        'stockroom.productrelationship': {
            'Meta': {'object_name': 'ProductRelationship'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'from_product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_product'", 'to': "orm['stockroom.Product']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_product'", 'to': "orm['stockroom.Product']"})
        },
        'stockroom.stockitem': {
            'Meta': {'object_name': 'StockItem'},
            'color': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stockroom.Color']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measurement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stockroom.Measurement']", 'null': 'True', 'blank': 'True'}),
            'package_count': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stockroom.Product']"})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['stockroom']
