# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Brand.description'
        db.alter_column('stockroom_brand', 'description', self.gf('django.db.models.fields.TextField')(null=True))


    def backwards(self, orm):
        
        # Changing field 'Brand.description'
        db.alter_column('stockroom_brand', 'description', self.gf('django.db.models.fields.CharField')(max_length=120))


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
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stockroom.Manufacturer']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'stockroom.cart': {
            'Meta': {'object_name': 'Cart'},
            'checked_out': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'stockroom.productcategory': {
            'Meta': {'object_name': 'ProductCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stockroom.ProductCategory']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'})
        },
        'stockroom.productgallery': {
            'Meta': {'object_name': 'ProductGallery'},
            'color': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stockroom.Color']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images_available': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stockroom.Product']"})
        },
        'stockroom.productimage': {
            'Meta': {'object_name': 'ProductImage'},
            'caption': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'gallery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stockroom.ProductGallery']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
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
