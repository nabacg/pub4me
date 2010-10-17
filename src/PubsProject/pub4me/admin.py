from django.contrib import admin

from PubsProject.pub4me.models import Pub
from PubsProject.pub4me.models import City
from PubsProject.pub4me.models import PubUser
from PubsProject.pub4me.models import UserAction

class PubAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'city', 'ext_service_id_kk')
admin.site.register(Pub, PubAdmin)

class CityAdmin(admin.ModelAdmin):
    pass
admin.site.register(City, CityAdmin)

class PubUserAdmin(admin.ModelAdmin):
    pass
admin.site.register(PubUser, PubUserAdmin)

class UserActionAdmin(admin.ModelAdmin):
    list_display = ('time', 'user', 'action_type')
    list_display_links = ('action_type', 'time')
admin.site.register(UserAction, UserActionAdmin)
