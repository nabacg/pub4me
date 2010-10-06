from django.conf.urls.defaults import *
from django.conf import settings
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
   
urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^', include('PubsProject.pub4me.urls')),
)

# serwowanie statycznych zasobow przez serwer deweloperski
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'site_media').replace('\\','/')}),
    )
