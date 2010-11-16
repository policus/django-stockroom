from django.conf.urls.defaults import *
from api import urls as api_urls

urlpatterns = patterns('',
    url(r'^', include(api_urls)),
)
