from django import forms
from .models import Permit
from permit_types.models import PermitType
from clients.models import Client

class PermitForm(forms.ModelForm):
    class Meta:
        model = Permit
        fields = (
            'description',
            'address',
            'company_name',
            'deposit_number',
            'client',
            'permit_type',
            'creation_date',
            'issue_date',
        )

        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),  # Text area for description
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'deposit_number': forms.NumberInput(attrs={'class': 'form-control'}),  # Number input for deposit number
            'client': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for client
            'permit_type': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for permit type
            'creation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # Date input for creation date
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # Date input for issue date'
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user 
        self.fields['client'].queryset = Client.objects.filter(active=True)
        self.fields['permit_type'].queryset = PermitType.objects.filter(active=True)
