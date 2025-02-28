from django import forms
from .models import PermitTypes

class PermitTypesForm(forms.ModelForm):

    class Meta:
        model = PermitTypes
        fields = (
            'name',
            'price',
            'active',
        )