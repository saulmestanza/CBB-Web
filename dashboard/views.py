from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.list import ListView

from utils.mixins import MultiGroupRequiredMixin
from dashboard.forms import *
from dashboard.models import *


class UsersListView(LoginRequiredMixin, MultiGroupRequiredMixin, ListView):
    model = User
    template_name = 'dashboard/users_list.html'
    context_object_name = 'users' 
    login_url = ''
    redirect_field_name = 'next' 
    groups_required = ["Administrador",]
    
    def get_queryset(self):
        return super().get_queryset().all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
