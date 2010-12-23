from django.conf.urls.defaults import *
from django.conf import settings
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
   
urlpatterns = patterns('',
    (r'^backstage2/', include(admin.site.urls)),
    (r'^', include('users.urls')),
    (r'^', include('pub4me.urls')),
    #(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'site_media').replace('\\','/')})
)

# serwowanie statycznych zasobow przez serwer deweloperski
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'site_media').replace('\\','/')}),
        #(r'site_media/(?P<path>[a-zA-Z0-9].*)$', 'django.views.static.serve', {'document_root': settings.STATIC_MEDIA_ROOT}),
    )
