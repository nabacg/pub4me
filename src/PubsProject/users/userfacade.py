from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from pub4me.models import PubUser
from django.conf import settings
import random


def create(user_name, password, is_guest = False, authenticate_user = False):
    new_user = User()
    if is_guest:
        #TODO: W taki sposob nie moge przydzielac ID gosciom. Co z tym zrobic?
        user_name = 'guest_' + str(random.randint(0,1000000000))
        password = settings.GUEST_USER_AUTO_PASSWORD
        
    new_user.username = user_name
    new_user.set_password(password)
    new_user.save()
    
    if not is_guest:
        #Zaznaczam, ze user nie jest gosciem tylko podal login i haslo
        pub_user = PubUser.objects.get(user = new_user.id)
        pub_user.registered = True
        pub_user.save()
    
    if authenticate_user:
        new_user = authenticate(username = new_user.username, password = password)
    return new_user

def create_and_login(user_name, password, request, is_guest = False):
    user = create(user_name, password, is_guest, authenticate_user = True)
    login(request, user)
    return user

def connect_with_facebook(user, fb_id, fb_first_name, fb_last_name):
    pub_user = PubUser.objects.get(user=user.id)
    pub_user.fb_id = fb_id
    pub_user.fb_first_name = fb_first_name
    pub_user.fb_last_name = fb_last_name
    pub_user.save()
    return pub_user