from django import forms
from .models import Permit

class PermitForm(forms.ModelForm):
    class Meta:
        model = Permit
        fields = '__all__' 
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'expiration_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'creation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
