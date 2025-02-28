from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DeleteView
from django.db.models import Q
from django.http import Http404

from django.urls import reverse_lazy

from utils.mixins import MultiGroupRequiredMixin
from users.forms import *


class UsersListView(LoginRequiredMixin, MultiGroupRequiredMixin, ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users' 
    login_url = ''
    redirect_field_name = 'next' 
    groups_required = ["Administrador",]
    paginate_by = 15
    
    def get_queryset(self):
        queryset = super().get_queryset().all()
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query) | 
                Q(first_name__icontains=search_query) | 
                Q(last_name__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class UsersCreateView(LoginRequiredMixin, MultiGroupRequiredMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'users/users_form.html'
    success_url = reverse_lazy('users_list')
    groups_required = ["Administrador",]


class UsersUpdateView(LoginRequiredMixin, MultiGroupRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/users_form.html'
    success_url = reverse_lazy('users_list')
    groups_required = ["Administrador",]


class UsersDeleteView(LoginRequiredMixin, MultiGroupRequiredMixin, DeleteView):
    model = User
    groups_required = ["Administrador",]
    success_url = reverse_lazy('users_list')

    
    def get_object(self):
        if not User.objects.filter(pk=self.kwargs['pk']).exists():
            raise Http404
        user = User.objects.get(pk=self.kwargs['pk'])
        return user

    
    def get(self, request, *args, **kwargs):
        user = self.get_object() 
        user.is_active = False
        user.save()
        return redirect(self.success_url)
    

class UserPasswordResetView(LoginRequiredMixin, MultiGroupRequiredMixin, UpdateView):
    model = User
    form_class = UserPasswordResetForm
    template_name = 'users/user_password_reset.html'
    success_url = reverse_lazy('users_list')
    groups_required = ["Administrador",]

    def form_valid(self, form):
        user = form.instance
        user.password = make_password(form.cleaned_data['new_password'])
        user.save()
        return super().form_valid(form)