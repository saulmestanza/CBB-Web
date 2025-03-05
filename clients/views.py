from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.http import Http404
from django.db.models import Q

from utils.mixins import MultiGroupRequiredMixin
from .models import *
from .forms import *


class ClientsListView(MultiGroupRequiredMixin, ListView):
    model = Client
    template_name = 'clients/clients_list.html'
    context_object_name = 'clients' 
    login_url = ''
    redirect_field_name = 'next' 
    groups_required = ["Administrador",]
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset().all().order_by('name')
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(national_id__icontains=search_query) | 
                Q(last_name__icontains=search_query)
            )

        filter_value = self.request.GET.get('filter', None)        
        if filter_value:
            queryset = queryset.filter(active=filter_value)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        user_group_names = self.request.user.groups.values_list('name', flat=True)
        context['user_group_names'] = user_group_names
        return context
    

class ClientsDeleteView(MultiGroupRequiredMixin, DeleteView):
    model = Client
    groups_required = ["Administrador",]
    success_url = reverse_lazy('clients_list')

    
    def get_object(self):
        if not Client.objects.filter(pk=self.kwargs['pk']).exists():
            raise Http404
        permit_type = Client.objects.get(pk=self.kwargs['pk'])
        return permit_type

    
    def get(self, request, *args, **kwargs):
        # permit_type = self.get_object() 
        # permit_type.active = False
        # permit_type.save()
        return redirect(self.success_url)


class ClientsCreateView(MultiGroupRequiredMixin, CreateView):
    model = Client
    groups_required = ["Administrador",]
    template_name = 'clients/clients_form.html'
    fields = ['name', 'last_name', 'national_id'] 
    success_url = reverse_lazy('clients_list') 

    def form_valid(self, form):
        form.instance.active = True
        return super().form_valid(form)
    

class ClientsUpdateView(MultiGroupRequiredMixin, UpdateView):
    model = Client
    groups_required = ["Administrador",]
    template_name = 'clients/clients_form.html'
    fields = ['name', 'last_name', 'national_id', 'active'] 
    success_url = reverse_lazy('clients_list') 

    def form_valid(self, form):
        return super().form_valid(form)