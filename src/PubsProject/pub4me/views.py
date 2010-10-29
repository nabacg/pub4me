from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import simplejson
from PubsProject.pub4me.models import Pub
from PubsProject.pub4me.forms import PubForm
from django.forms.formsets import formset_factory


def index(request):
    PubFormSet = formset_factory(PubForm, extra=1, max_num=5)
    formset = PubFormSet()
    return render_to_response('pub4me/index.html', {"user_name": request.user.username, "formset": formset}, context_instance=RequestContext(request))

''' DO WYWALENIA jezeli mege kremos-grzesiek sie zakonczy
def index(request):
    params = {}
    if request.user.is_authenticated():
        params['user_name'] = request.user.username
    return render_to_response('pub4me/index.html', params, context_instance=RequestContext(request))
'''

def pub_recommend(request):
    PubFormSet = formset_factory(PubForm, extra=1, max_num=5)
    if request.method == "POST":
        formset = PubFormSet(request.POST)        
        return HttpResponse("TODO")

def pub_autocomplete(request):
    if request.method == 'GET':
        if request.GET.__contains__('term'):
            term = request.GET.__getitem__('term')
            query_result = Pub.objects.filter(name__icontains=term)[:10]
            
            json_data = simplejson.dumps(map(lambda r : {
                    "id": r.pk,
                    "label": "%s - %s" % (r.name, r.location),
                    "value": "%s - %s" % (r.name, r.location)},
                query_result))
            return HttpResponse(json_data,'application/javascript')
    err_msg = "Unable to find Pub 4 you.."
    return HttpResponse(simplejson.dumps({"err_msg": err_msg}))