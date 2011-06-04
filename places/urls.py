from django.conf.urls.defaults import *

urlpatterns = patterns('places.views',
    url(r'^(?P<pk>\d+)/$', 'place_detail', name='place_detail'),
)