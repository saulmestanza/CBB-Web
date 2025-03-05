from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.http import Http404

from utils.mixins import MultiGroupRequiredMixin
from .models import *
from .forms import *


class PermitTypesListView(MultiGroupRequiredMixin, ListView):
    model = PermitType
    template_name = 'permit_types/permit_types_list.html'
    context_object_name = 'permit_types' 
    login_url = ''
    redirect_field_name = 'next' 
    groups_required = ["Administrador",]
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset().all().order_by('name').order_by('-active')
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        user_group_names = self.request.user.groups.values_list('name', flat=True)
        context['user_group_names'] = user_group_names
        return context
    

class PermitTypesDeleteView(MultiGroupRequiredMixin, DeleteView):
    model = PermitType
    groups_required = ["Administrador",]
    success_url = reverse_lazy('permit_types_list')

    
    def get_object(self):
        if not PermitType.objects.filter(pk=self.kwargs['pk']).exists():
            raise Http404
        permit_type = PermitType.objects.get(pk=self.kwargs['pk'])
        return permit_type

    
    def get(self, request, *args, **kwargs):
        permit_type = self.get_object() 
        permit_type.active = False
        permit_type.save()
        return redirect(self.success_url)



class PermitTypesCreateView(MultiGroupRequiredMixin, CreateView):
    model = PermitType
    groups_required = ["Administrador",]
    template_name = 'permit_types/permit_types_form.html'
    fields = ['name', 'price', 'active'] 
    success_url = reverse_lazy('permit_types_list') 

    def form_valid(self, form):
        return super().form_valid(form)
    

class PermitTypesUpdateView(MultiGroupRequiredMixin, UpdateView):
    model = PermitType
    groups_required = ["Administrador",]
    template_name = 'permit_types/permit_types_form.html'
    fields = ['name', 'price', 'active'] 
    success_url = reverse_lazy('permit_types_list')

    def form_valid(self, form):
        return super().form_valid(form)