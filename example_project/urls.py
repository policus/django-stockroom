from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from tastypie.api import Api
from example_project.apps.stockroom.api import ProductCategoryResource, CartResource

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(ProductCategoryResource())
v1_api.register(CartResource())

urlpatterns = patterns('',
    url(r'^$', 'example_project.views.cart_test', name='cart_test'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root' : settings.MEDIA_ROOT }
    ),
    url(r'^api/', include(v1_api.urls)),
)
