from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import simplejson
from PubsProject.pub4me.models import Pub
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from PubsProject.pub4me.forms import PubUserForm
from PubsProject.pub4me.forms import PubForm

@login_required
def index(request):
    form = PubForm()
    return render_to_response('pub4me/index.html', {"user_name": request.user.username, 'form': form}, context_instance=RequestContext(request))

#te 2 widoki przenioslbym do osobnej aplikacji UserManagement
def logout_view(request):
    logout(request)
    return render_to_response('registration/login.html', {"form" : AuthenticationForm()}, context_instance=RequestContext(request))

def sign_up(request):
    if request.method == "POST":
#ajaj ale to brzydko zrobione jest.. 
       # request.POST["password"] = hash(request.POST["password"])
        sign_up_form = UserCreationForm(request.POST)
        if sign_up_form.is_valid():
#            user =
            sign_up_form.save()
#            user.password = hash(user.password)
#            user.save()
            return render_to_response('registration/login.html', {"form" : AuthenticationForm()}, context_instance=RequestContext(request))
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