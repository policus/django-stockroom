from django.conf import settings
from collections import Counter
import os

if settings.STOCKROOM_PRODUCT_THUMBNAIL_SIZES:
    PRODUCT_THUMBNAILS = settings.STOCKROOM_PRODUCT_THUMBNAIL_SIZES
else:
    PRODUCT_THUMBNAILS = None
    
def build_thumbnail_list(gallery_object):
    images = []
    for i in gallery_object.images.all():
        head, tail = os.path.split(i.image.url)
        filename, ext = os.path.splitext(tail)
        sizes = {}
        for s in PRODUCT_THUMBNAILS:
            size = {
                'width' : s[0],
                'height' : s[1],
                'url' : "%s/%s.%sx%s%s" % (head, filename, s[0], s[1], ext)
            }
            sizes.update({
                '%sx%s' % (s[0], s[1]) : size,
            })
            
        image = {
            'caption' : i.caption,
            'sizes' : sizes,
        }
        images.append(image)
    return images

def structure_products(product_object):
    
    if getattr(product_object, '__iter__', False):
        response = []
        # Collect images and inventory for each object
        for p in product_object:

            galleries = []
            for g in p.gallery.all():
                images = []
                for i in g.images.all():
                    image = {
                        'url' : i.image.url,
                    }
                    images.append(i)
            
                gallery = {
                    'color' : g.color,
                    'images' : images,
                }
                galleries.append(gallery)
        
            stock = []
            available_sizes = Counter()
            available_colors = Counter()
            for s in p.stock.all():
                available_sizes[s.measurement] += 1
                available_colors[s.color] += 1
                stock_item = {
                    'size' : {
                        'measurement' : s.measurement.measurement,
                        'unit' : {
                            'name' : s.measurement.unit.name,
                            'abbreviation' : s.measurement.unit.abbreviation,
                        },
                    },
                    'color' : {
                        'name' : s.color.name,
                        'red' : s.color.red,
                        'green' : s.color.green,
                        'blue' : s.color.blue,
                        'swatch' : s.color.swatch,
                    },
                    'package_count' : s.package_count,
                    'price_override': s.price,
                
                }
                stock.append(stock_item)
                
            
            item = {
                'id' : p.pk,
                'title' : p.title,
                'description' : p.description,
                'price' : p.get_price(),
                'sku' : p.sku,
                'tags' : p.tags.all(),
                'category' : {
                    'id' : p.category.pk,
                    'name' : p.category.name,
                    'slug' : p.category.slug,
                },
                'brand' : {
                    'id' : p.brand.pk,
                    'name' : p.brand.name,
                    'manufacturer' : {
                        'id' : p.brand.manufacturer.pk,
                        'name' : p.brand.manufacturer.name,
                    },
                },
                'galleries' : galleries,
                'inventory' : {
                    'stock' : stock,
                    'available_colors' : available_colors,
                    'available_sizes' : available_sizes,
                },
            }

            response.append(item)
        

    else:
        galleries = product_object.gallery.all()
        stock = product_object.stock.all()
        available_sizes = Counter()
        available_colors = Counter()
        for s in stock:
            available_sizes[s.measurement] += 1
            available_colors[s.color] += 1
        
            
        response = {
            'id' : product_object.pk,
            'title' : product_object.title,
            'description' : product_object.description,
            'price' : product_object.get_price(),
            'sku' : product_object.sku,
            'tags' : product_object.tags.all(),
            'category' : {
                'id' : product_object.category.pk,
                'name' : product_object.category.name,
                'slug' : product_object.category.slug,
            },
            'brand' : {
                'id' : product_object.brand.pk,
                'name' : product_object.brand.name,
                'manufacturer' : {
                    'id' : product_object.brand.manufacturer.pk,
                    'name' : product_object.brand.manufacturer.name,
                },
            },
            'galleries' : galleries,
            'inventory' : {
                'stock' : stock,
                'available_colors' : available_colors,
                'available_sizes' : available_sizes,
            },
        }
    
    return response

def structure_gallery(gallery_object):
    
    if getattr(gallery_object, '__iter__', False):
        response = []
        for g in gallery_object:        
            images = []
            for i in g.images.all():
                image = {
                    'caption' : i.caption,
                    'image' : i.image,
                }
                images.append(image)
            
            gallery = {
                'id' : g.pk,
                'images_available' : g.images_available,
                'images' : images,
                'color' : g.color,
            }
            response.append(gallery)
        
    else:
        response = {
            'id' : gallery_object.pk,
            'images_available' : gallery_object.images_available,
            'color' : gallery_object.color,
            'images' : build_thumbnail_list(gallery_object),
        }
    
    return response