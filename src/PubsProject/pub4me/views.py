from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import simplejson
from PubsProject.pub4me.models import Pub
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from PubsProject.users.userfacade import create, create_and_login

def index(request):
    params = {}
    if request.user.is_authenticated():
        params['user_name'] = request.user.username
    return render_to_response('pub4me/index.html', params, context_instance=RequestContext(request))

#te 2 widoki przenioslbym do osobnej aplikacji UserManagement
def logout_view(request):
    logout(request)
    return render_to_response('registration/login.html', {"form" : AuthenticationForm()}, context_instance=RequestContext(request))

def sign_up(request):
    if request.method == "POST":
        sign_up_form = UserCreationForm(request.POST)
        if sign_up_form.is_valid():
            #sign_up_form.save()
            #user = create(sign_up_form.data['username'], sign_up_form.data['password1'], authenticate_user = True)
            #user = authenticate(username = user.username, password = sign_up_form.data['password1'])
            #login(request, user)
            user = create_and_login(sign_up_form.data['username'], sign_up_form.data['password1'], request)
            return render_to_response('pub4me/index.html', {"user_name": user.username }, context_instance=RequestContext(request))
    else:
        sign_up_form = UserCreationForm()
    return render_to_response('registration/login.html', {'sign_up_form':sign_up_form}, context_instance=RequestContext(request))
#az dotad ;)

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