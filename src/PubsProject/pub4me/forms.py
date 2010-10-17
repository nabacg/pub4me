from django.forms import ModelForm, HiddenInput
from PubsProject.pub4me.models import PubUser
from PubsProject.pub4me.models import Pub


class PubUserForm(ModelForm):
    class Meta:
        model = PubUser
        fields = ('username', 'email', 'password')
        
class PubForm(ModelForm):
    class Meta:
        model = Pub
        widgets = {
                   'location' : HiddenInput(), 
                   'city' : HiddenInput(),
                   'ext_service_id_kk' : HiddenInput()                   
                   }