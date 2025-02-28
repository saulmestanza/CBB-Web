from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy

from dashboard.forms import *
from dashboard.models import *


class LogInView(LoginView):
    template_name = "auth/login.html"
    authentication_form = AuthenticationForm

    def get_success_url(self):
        user = self.request.user
        if user.is_staff:
            return reverse_lazy('users_list')
        return reverse_lazy('users_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None and user.is_active:
            login(self.request, user)
            next_url = self.request.GET.get('next', self.get_success_url())
            return redirect(next_url)
        else:
            messages.error(self.request, ("Cuenta deshabilitada."))
            return self.form_invalid(form)
        
    def form_invalid(self, form):
        messages.error(self.request, ("Usuario o contraseña incorrecta."))
        return self.render_to_response(self.get_context_data(form=form))
    
    
class LogOutView(LogoutView):

    def post(self, request, *args, **kwargs):
        logout(request) 
        return redirect("login")  


class UsersListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'dashboard/users_list.html'
    context_object_name = 'users' 
    login_url = ''
    redirect_field_name = 'next' 

    def test_func(self):
        return self.request.user.is_superuser
    
    def get_queryset(self):
        return super().get_queryset().all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
