from django.views.generic.simple import direct_to_template

def cart_test(request):
    return direct_to_template(request, 'home.html', {
        'cart' : request.cart
    })