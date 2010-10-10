from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
#from django.core import serializers
from django.utils import simplejson
from PubsProject.pub4me.models import Pub



def index(request):
    return render_to_response('pub4me/index.html', context_instance=RequestContext(request))

def pub_autocomplete(request):
    
    # p = get_object_or_404(Poll, pk=poll_id)
    if request.method == 'GET':
        if request.GET.__contains__('term'):
            term = request.GET.__getitem__('term')
            suggestions = []
            query_result = Pub.objects.filter(name__icontains=term)[:10]
            for obj in query_result:
                suggestions.append({"id": obj.pk, "label": obj.name + " - " + obj.location, "value": obj.name + " - " + obj.location})
            #result = [ {x.name , x.location} for x in query_result ]
            #json_data = serializers.serialize('json', suggestions)
            json_data = simplejson.dumps(suggestions)
            return HttpResponse(json_data,'application/javascript')


    return render_to_response('pub4me/pub_autocomplete_json.html', {'term': 'chuja-zle wywoalenie'}, context_instance=RequestContext(request))
    
