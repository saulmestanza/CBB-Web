from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.http import Http404

from utils.mixins import MultiGroupRequiredMixin
from .models import *
from .forms import *


class PermitTypesListView(LoginRequiredMixin, MultiGroupRequiredMixin, ListView):
    model = PermitTypes
    template_name = 'permit_types/permit_types_list.html'
    context_object_name = 'permit_types' 
    login_url = ''
    redirect_field_name = 'next' 
    groups_required = ["Administrador",]
    paginate_by = 15
    
    def get_queryset(self):
        return super().get_queryset().all().order_by('name').order_by('-active')
    

class PermitTypesDeleteView(LoginRequiredMixin, MultiGroupRequiredMixin, DeleteView):
    model = PermitTypes
    groups_required = ["Administrador",]
    success_url = reverse_lazy('permit_types_list')

    
    def get_object(self):
        if not PermitTypes.objects.filter(pk=self.kwargs['pk']).exists():
            raise Http404
        permit_type = PermitTypes.objects.get(pk=self.kwargs['pk'])
        return permit_type

    
    def get(self, request, *args, **kwargs):
        permit_type = self.get_object() 
        permit_type.active = False
        permit_type.save()
        return redirect(self.success_url)



class PermitTypesCreateView(LoginRequiredMixin, MultiGroupRequiredMixin, CreateView):
    model = PermitTypes
    groups_required = ["Administrador",]
    template_name = 'permit_types/permit_types_form.html'
    fields = ['name', 'price', 'active'] 
    success_url = reverse_lazy('permit_types_list') 

    def form_valid(self, form):
        form.instance.active = True 
        return super().form_valid(form)
    

class PermitTypesUpdateView(LoginRequiredMixin, MultiGroupRequiredMixin, UpdateView):
    model = PermitTypes
    groups_required = ["Administrador",]
    template_name = 'permit_types/permit_types_form.html'
    fields = ['name', 'price', 'active'] 
    success_url = reverse_lazy('permit_types_list')

    def form_valid(self, form):
        return super().form_valid(form)