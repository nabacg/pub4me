from django.conf.urls.defaults import *
from django.conf import settings
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
   
urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
#TO tutaj specjalnie w tym url.py bo mysle zeby przeniesc te widoki do osobnej aplikacji UserManagement
    #LOGIN VIEW
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    #LOGOUT
    (r'^logout/', 'PubsProject.pub4me.views.logout_view'),
    (r'^sign/$', 'PubsProject.pub4me.views.sign_up'),
    (r'^', include('PubsProject.pub4me.urls')),
    #(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'site_media').replace('\\','/')})
)

# serwowanie statycznych zasobow przez serwer deweloperski
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'site_media').replace('\\','/')}),
        #(r'site_media/(?P<path>[a-zA-Z0-9].*)$', 'django.views.static.serve', {'document_root': settings.STATIC_MEDIA_ROOT}),
    )
