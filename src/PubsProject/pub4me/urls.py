from django.conf.urls.defaults import *
from django.views.generic import list_detail
from pub4me.models import Pub

info_dict = {
    'queryset': Pub.objects.filter(active = True),
}

urlpatterns = patterns('pub4me.views',
    (r'^$', 'index'),
    (r'^all_pubs$', list_detail.object_list, info_dict), #Niepotrzebne - do wywalenia
    (r'^pub_autocomplete$', 'pub_autocomplete'),
    (r'^pub_recommend$', 'pub_recommend'),
    (r'^pub_selected$', 'pub_selected'),
    (r'^pub_create$', 'pub_create'),
    (r'^facebook$', 'facebook'),
    (r'^facebook_canvas$', 'facebook_canvas'),
    (r'^refresh_cache$', 'refresh_cache'),
    # (r'^(?P<poll_id>\d+)/$', 'detail'),
    # (r'^(?P<poll_id>\d+)/results/$', 'results'),
    # (r'^(?P<poll_id>\d+)/vote/$', 'vote')
)