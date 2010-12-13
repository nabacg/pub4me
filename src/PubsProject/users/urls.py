from django.conf.urls.defaults import *

urlpatterns = patterns('',
    #LOGIN VIEW
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    #LOGOUT
    (r'^logout/', 'users.views.logout_view'),
    (r'^sign/$', 'users.views.sign_up'),
)