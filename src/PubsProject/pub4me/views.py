from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
#from django.core import serializers
from django.utils import simplejson
from PubsProject.pub4me.models import Pub



def index(request):
    return render_to_response('pub4me/index.html', context_instance=RequestContext(request))

def pub_autocomplete(request):
    if request.method == 'GET':
        if request.GET.__contains__('term'):
            term = request.GET.__getitem__('term')
#            suggestions = []
            query_result = Pub.objects.filter(name__icontains=term)[:10]
#            for obj in query_result:
#                suggestions.append({"id": obj.pk, "label": obj.name + " - " + obj.location, "value": obj.name + " - " + obj.location})
            json_data = simplejson.dumps(map(lambda r : {
                    "id": r.pk,
                    "label": "%s - %s" % (r.name, r.location),
                    "value": "%s - %s"%(r.name, r.location)}),
                query_result)
            return HttpResponse(json_data,'application/javascript')
    return render_to_response('pub4me/pub_autocomplete_json.html', {'term': 'Error'}, context_instance=RequestContext(request))
