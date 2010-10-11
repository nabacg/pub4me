from django.forms import ModelForm
from pub4me.models import PubUser

class PubUserForm(ModelForm):
    class Meta:
        model = PubUser
        fields = ('username', 'email', 'password')