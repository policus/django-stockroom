jQuery(document).ready(function($) {

function CategoryResource(category_slug){
    this.list = function(){
        var categories = $.ajax({
            type: 'GET',
            url: '/stockroom/api/categories/',
            async: false,
            dataType: 'json'
        });
        return $.parseJSON(categories.responseText);
    }
    
    this.get = function(category_slug){
        var category = $.ajax({
            type: 'GET',
            url: '/stockroom/api/categories/' + category_slug + '/',
            async: false,
            dataType: 'json'
        });
        return $.parseJSON(category.responseText);
    }
    
}

function ProductResource(parameter){
    this.list = function(){
        var products = $.ajax({
            type: 'GET',
            url: '/stockroom/api/products/',
            async: false,
            dataType: 'json'
        });
        return $.parseJSON(products.responseText);
    }
    
    this.get = function(parameter){
        var pk = parameter.pk.toString();
        var product = $.ajax({
            type: 'GET',
            url: '/stockroom/api/products/' + pk + '/',
            async: false,
            dataType: 'json'
        });
        return $.parseJSON(product.responseText);
    }
    
    this.inventory = function(parameter){
        var pk = parameter.pk.toString();
        var inventory = $.ajax({
            type: 'GET',
            url: '/stockroom/api/products/' + pk + '/inventory/',
            async: false,
            dataType: 'json'
        });
        return $.parseJSON(inventory.responseText);
    }
    
}

function CartResource(parameter){
    
    var request_url = '/stockroom/api/cart/';
    
    this.list = function(successCallback, errorCallback){
        var cart = $.ajax({
            type: 'GET',
            url: request_url,
            async: true,
            dataType: 'json',
            error: function(request, error){
                errorCallback();
            },
            success: function(data, successCallback){
                successCallback(data);
            }
        });
    }
    
    this.get = function(parameter, callbacks){
        var pk = parameter.cart_item;
        var cart_item = $.ajax({
            type: 'GET',
            url: request_url + pk,
            async: true,
            dataType: 'json',
            error: function(request, status){
                console.log(request, status);
                return false;
            },
            success: function(data){
                console.log(data);
                return data.responseText;
            }
        });
    }
    
    this.add = function(parameter){
        var stock_item = parameter.stock_item;
        var quantity = parameter.quantity;
        var cart = $.ajax({
            type: 'PUT',
            url: request_url,
            async: false,
            dataType: 'json',
            data: {
                stock_item: stock_item,
                quantity: quantity
            }
        });
        console.log(cart.responseText);
        return cart.responseText;
    }
    
        
}

// Usage Examples
var cart_resource = new CartResource();
var product_resource = new ProductResource();

var products = product_resource.list();
console.log(products);

var p = product_resource.get({pk:1})
console.log(p);


}); // close jQuery scope