from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from PubsProject.users.userfacade import create_and_login
from django.shortcuts import render_to_response
from django.template import RequestContext

def logout_view(request):
    logout(request)
    return render_to_response('registration/login.html', {"form" : AuthenticationForm()}, context_instance=RequestContext(request))

def sign_up(request):
    if request.method == "POST":
        sign_up_form = UserCreationForm(request.POST)
        if sign_up_form.is_valid():
            user = create_and_login(sign_up_form.data['username'], sign_up_form.data['password1'], request, False)
            return render_to_response('pub4me/index.html', {"user_name": user.username }, context_instance=RequestContext(request))
    else:
        sign_up_form = UserCreationForm()
    return render_to_response('registration/login.html', {'sign_up_form':sign_up_form}, context_instance=RequestContext(request))