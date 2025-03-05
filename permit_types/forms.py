from django import forms
from .models import PermitType

class PermitTypesForm(forms.ModelForm):

    class Meta:
        model = PermitType
        fields = (
            'name',
            'price',
            'active',
        )