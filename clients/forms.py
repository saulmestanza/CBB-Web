from django import forms
from .models import Client

class ClientsForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = (
            'name',
            'last_name',
            'national_id',
        )