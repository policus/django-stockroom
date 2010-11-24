def structure_products(products):
    response = []

    for p in products:
        # Collect image galleries
        galleries = []
        for g in p.gallery.all():
            images = []
            for i in g.image.all():
                image = {
                    'url' : i.image.url,
                }
                images.append(i)
            
            gallery = {
                'color' : g.color,
                'images' : images,
            }
            galleries.append(gallery)
        
        # Collect inventory
        inventory = []
        for s in p.stock.all():
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
            inventory.append(stock_item)
    
        
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
            'inventory' : inventory,
        }
        
        response.append(item)
        
            
    return response