from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings

class City(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    pl_name = models.CharField(max_length=100)
    en_name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.pl_name
     
class Pub(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    city = models.ForeignKey(City, default = settings.DEFAULT_CITY_ID)
    active = models.BooleanField(default = True)
    ext_service_id_kk = models.BigIntegerField(default = settings.DEFAULT_EXT_SERVICE_ID) # ID knajpy z serwisu zewnetrzego (knajpy.krakow.pl)
    def __unicode__(self):
        return self.name


class PubUser(models.Model):
    user = models.ForeignKey(User)
#   email = models.EmailField(max_length=100)
    registered = models.BooleanField(default=False)
#   time_registered = models.TimeField()
#   time_setup = models.TimeField()
    fb_id = models.BigIntegerField(null=True)
    fb_first_name = models.CharField(max_length=100)
    fb_last_name = models.CharField(max_length=100)
    pubs = models.ManyToManyField(Pub)

    def __unicode__(self):
        return "PubUser for %s" % self.user.username
    
    def nice_name(self):
        if self.registered:
            return self.user.username
        elif self.fb_id:
            return self.fb_first_name
        else: #auto user
            return None 
        
    def create_pub_user(sender, instance, created, **kwargs):
        if created:
            PubUser.objects.get_or_create(user = instance)

    post_save.connect(create_pub_user, sender=User)
    
class UserAction(models.Model): 
    USER_ACTION_TYPES = (
        (u'LP', u'User liked a pub'),
        (u'GS', u'User got a suggestion'),
    )
    user = models.ForeignKey(PubUser)
    ip = models.IPAddressField()
    time = models.DateTimeField(auto_now_add=True)
    browser_info = models.CharField(max_length=500)
    referer = models.URLField()
    languages = models.CharField(max_length=100)
    action_type = models.CharField(max_length=3, choices=USER_ACTION_TYPES)
    
class UserAction_LikedPub(UserAction):
    #useraction = models.OneToOneField(UserAction, primary_key=True)
    pub = models.ForeignKey(Pub)

class UserAction_GotSuggestion(UserAction):
    #useraction = models.OneToOneField(UserAction, primary_key=True)
    pub = models.ForeignKey(Pub) # Jezeli rekomendujemy wiecej niz jedna knajpe na raz, to trzeba wydzielic osobna tabele many-to-one