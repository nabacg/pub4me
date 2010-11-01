from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from PubsProject.pub4me.models import PubUser

def create(user_name, password,  authenticate_user = False):
    new_user = User()
    new_user.username = user_name
    new_user.set_password(password)
    new_user.save()
    if authenticate_user:
        new_user = authenticate(username = new_user.username, password = password)
    return new_user

def create_and_login(user_name, password, request):
    user = create(user_name, password, authenticate_user = True)
    login(request, user)
    return user

def connect_with_facebook(user, fb_id, fb_first_name, fb_last_name):
    pub_user = PubUser.objects.get(user=user.id)
    pub_user.update(fb_id=fb_id, fb_first_name=fb_first_name, fb_last_name=fb_last_name)
    return pub_user