from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from pub4me.models import Pub
from pub4me.models import PubUser, UserAction_LikedPub, UserAction_GotSuggestion
from pub4me.forms import PubForm
from users.userfacade import connect_with_facebook, create_and_login
from django.forms.formsets import formset_factory
from django.conf import settings
import urllib
import cgi
import time
from django.utils import simplejson as json
from django.shortcuts import get_object_or_404
from pub4me import recommendations

def index(request):
    if not request.user.is_authenticated():
        create_and_login(None, None, request, is_guest = True)
    request.session.set_expiry(60*60*24*365*2)  #sesja wygasnie za 2 lata, 
                                                #    bo plota glosi ze 10 letnie ciastka nie sa lubiane przez przegladarki :)
    
    PubFormSet = formset_factory(PubForm, extra=1, max_num=5)
    formset = PubFormSet()
    username = PubUser.objects.get(user=request.user.id).nice_name()
    return render_to_response('pub4me/index.html', {"user_name": username, "formset": formset}, context_instance=RequestContext(request))

# wymusza odswiezenie cache
def refresh_cache(request):
    return HttpResponse(json.dumps(recommendations.refresh_cache()))
    
def pub_recommend(request):
    PubFormSet = formset_factory(PubForm, extra=1, max_num=5)
    
    if request.method == "POST":
        #formset = PubFormSet(request.GET) 
        selected_pubs = {}
        data =  request.POST
        for field in data.keys():
            pub_name = data[field].split('-')
            pub_name = unicode("-".join(pub_name[0:-1]).strip())
            if pub_name != "":
                selected_pubs[pub_name] = 1
    print selected_pubs
    topPubs = recommendations.get_top_matches(selected_pubs)#request.user.pubuser_set.all()[0])
    #pub_id = Pub.objects.all()[4].id    
    for ranking, pub in topPubs:
        pub_id = Pub.objects.get(name = pub).id
        save_user_action(request, pub_id , 'GS')       
    return HttpResponse(json.dumps(map(lambda p: p[1], topPubs)))
    
def pub_selected(request):
    pub_id = request.REQUEST['id']

    save_user_action(request, pub_id, 'LP')
    
    return HttpResponse(json.dumps({"success": True}))

# to nie jest view,metoda pomocnicza
# przeniesc gdzei indziej

def save_user_action(request, pub_id, action_type):
    if action_type == 'LP':
        action = UserAction_LikedPub()
    else: 
        action = UserAction_GotSuggestion()
    action.pub = get_object_or_404(Pub, pk=pub_id)
    action.user = request.user.pubuser_set.all()[0]
    action.ip = request.META['REMOTE_ADDR']
    action.time = time.ctime()
    action.browser_info = request.META['REMOTE_ADDR']
    action.referer = request.path
    action.languages = request.META['HTTP_ACCEPT_LANGUAGE']
    action.action_type = action_type
    action.save()
    
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

def facebook_canvas(request):
    redirect_link = "http://" + request.get_host() + '/facebook'
    return render_to_response('pub4me/facebook_canvas.html', {'redirect_link': redirect_link})

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
            
            #Jezeli ten FB ID juz jest skojarzony z jakims innym kontem to tylko przelogowujemy usera na tamto konto
            if PubUser.objects.filter(fb_id__exact=long(fb_user_id)).count() > 0:
                logout(request)
                existing_user = PubUser.objects.get(fb_id__exact = long(fb_user_id)).user
                user_name = existing_user.username
                existing_user = authenticate(username = user_name, password = settings.GUEST_USER_AUTO_PASSWORD)
                login(request, existing_user)
                return HttpResponseRedirect('/')
            
            #W tym momencie znamy goscia dane z fejsa - min fejsowe ID. 
            this_user = request.user
            
            #Jezeli user jeszcze nie ma konta (chociazby automatycznie zakladanego) 
            #i nie jest zalogowany, to zakladymy konto i logujemy go na szybkosci
            #Jezeli gosc mial konto na login i haslo, a chce je polaczyc z FB, to tez zakladamy nowe, a poprzednie olewamy
            #Za duzo pieprzenia z laczeniem dwoch typow kont
            if (not this_user.is_authenticated()) or ((this_user.is_authenticated() and PubUser.objects.get(user = this_user.id).registered)):
                this_user = create_and_login(None, None, request, is_guest = True)
            
            connect_with_facebook(this_user, fb_user_id, fb_user_first_name, fb_user_last_name)
             
            return HttpResponseRedirect('/')
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

    