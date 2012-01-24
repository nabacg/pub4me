from django.forms import ModelForm, HiddenInput, TextInput
from pub4me.models import PubUser
from pub4me.models import Pub

'''
class PubUserForm(ModelForm):
    class Meta:
        model = PubUser
        fields = ('username', 'email', 'password')
'''
        
class PubForm(ModelForm):
    class Meta:
        model = Pub
        fields = ('id', 'name')
        widgets = {
                   'id' : HiddenInput(),
                   'name' : TextInput(attrs={'class':'autocomplete placename'})                
                   }