from django.conf.urls.defaults import *
from django.views.generic import list_detail
from PubsProject.pub4me.models import Pub

info_dict = {
    'queryset': Pub.objects.all(),
}

urlpatterns = patterns('PubsProject.pub4me.views',
    (r'^$', 'index'),
    (r'^all_pubs$', list_detail.object_list, info_dict),
    (r'^pub_autocomplete$', 'pub_autocomplete'),
    # (r'^(?P<poll_id>\d+)/$', 'detail'),
    # (r'^(?P<poll_id>\d+)/results/$', 'results'),
    # (r'^(?P<poll_id>\d+)/vote/$', 'vote')
)