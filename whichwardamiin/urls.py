from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from mapit.views.areas import area_polygon
from .views import Index, Postcode

# Admin section
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name='index'),
    url(r'^postcode/(?P<postcode>\w+)$', Postcode.as_view(), name='postcode'),
    url(r'^area/(?P<srid>[0-9]+)/(?P<area_id>[0-9]+)\.(?P<format>kml|json|geojson|wkt)$', area_polygon, name='area_polygon'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

