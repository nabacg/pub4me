from django.conf.urls.defaults import *
from django.views.generic import list_detail
from pub4me.models import Pub

info_dict = {
    'queryset': Pub.objects.all(),
}

urlpatterns = patterns('pub4me.views',
    (r'^$', 'index'),
    (r'^all_pubs$', list_detail.object_list, info_dict), #Niepotrzebne - do wywalenia
    (r'^pub_autocomplete$', 'pub_autocomplete'),
    (r'^pub_recommend$', 'pub_recommend'),
    (r'^facebook$', 'facebook'),
    # (r'^(?P<poll_id>\d+)/$', 'detail'),
    # (r'^(?P<poll_id>\d+)/results/$', 'results'),
    # (r'^(?P<poll_id>\d+)/vote/$', 'vote')
)