from django import forms
from .models import Clients

class ClientsForm(forms.ModelForm):

    class Meta:
        model = Clients
        fields = (
            'name',
            'last_name',
            'national_id',
        )