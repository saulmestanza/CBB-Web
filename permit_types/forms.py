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
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }