from django import forms
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password 

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Roles'
    )
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'password', 'is_active', 'groups',
        ]

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            try:
                validate_password(password)
            except ValidationError as e:
                raise forms.ValidationError(e.messages)

        return password
        
    def save(self, commit=True):
        user = super().save(commit=False)
        
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            user.groups.set(self.cleaned_data['groups']) 

        return user


class UserUpdateForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'is_active', 'groups'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
            user.groups.set(self.cleaned_data['groups']) 

        return user


class UserPasswordResetForm(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput, label="Nueva Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = User
        fields = ['new_password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data