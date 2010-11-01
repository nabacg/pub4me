from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from PubsProject.pub4me.models import Pub
from PubsProject.pub4me.forms import PubForm
from PubsProject.users.userfacade import connect_with_facebook
from django.forms.formsets import formset_factory
from django.conf import settings
import urllib
import cgi
from django.utils import simplejson as json

def index(request):
    PubFormSet = formset_factory(PubForm, extra=1, max_num=5)
    formset = PubFormSet()
    return render_to_response('pub4me/index.html', {"user_name": request.user.username, "formset": formset}, context_instance=RequestContext(request))

''' DO WYWALENIA jezeli merge kremos-grzesiek sie zakonczy
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

def facebook(request):
    if request.method == 'GET':
        this_url = "http://" + request.get_host() + request.path
        args = dict(client_id=settings.FACEBOOK_APP_ID, redirect_uri=this_url)
        if request.GET.__contains__('code'):
            args["code"] = request.GET.__getitem__('code') 
            args["client_secret"] = settings.FACEBOOK_APP_SECRET
            '''
            return HttpResponse(urllib.urlopen(
                "https://graph.facebook.com/oauth/access_token?" +
                urllib.urlencode(args)).read() + "<br/>\n code:"+args["code"] +"\n<br/>url:"+ "https://graph.facebook.com/oauth/access_token?" +
                urllib.urlencode(args) )
            '''
            #Strzal bezposrednio do FB. Pytamy o acces_token
            #Parametry: client_id, redirect_uri, code, client_secret
            fb_response = cgi.parse_qs(urllib.urlopen(
                "https://graph.facebook.com/oauth/access_token?" +
                urllib.urlencode(args)).read())
            
            access_token = fb_response["access_token"][-1]
            
            #Kolejny bezposredni strzal. 
            #Pobieramy z FB podstawowe dane usera
            profile = json.load(urllib.urlopen(
                "https://graph.facebook.com/me?" +
                urllib.urlencode(dict(access_token=access_token))))
            
            fb_user_id = str(profile["id"])
            fb_user_first_name = profile["first_name"]
            fb_user_last_name = profile["last_name"]
            
            #### TODO: W tym momencie znamy ID z fejsa. 
            #Tutaj trzeba je skojarzyc z kontem usera (ktore z zalozenia powinno juz byc automatycznie zalozone)
            this_user = request.user
            if not this_user.is_authenticated():
                create_and_login(user_name, password, request):
            pub_user = connect_with_facebook(this_user, fb_user_id, fb_user_first_name, fb_user_last_name)
            
                
            return HttpResponse("Twoj facebookowy ID: " + fb_user_id +", a na imie masz: " + fb_user_first_name)
        else:
            #Strzal do Fejsbuka (poprzez redirect).
            #User musi uprawnic nasza aplikacje wenatrz FB. 
            #Fejsbuk zwroci redirect na nas i da nam parametr CODE potrzebny za chwile
            #Parametry: client_id, redirect_uri
            return HttpResponseRedirect(
                "https://graph.facebook.com/oauth/authorize?" +
                urllib.urlencode(args));  
    else:
        return HttpResponse("BLAD: Obslugiwana jest tylko metoda GET")

    