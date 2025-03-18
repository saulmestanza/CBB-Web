import os
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404
from django.db.models import Q
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
from utils.mixins import MultiGroupRequiredMixin
from permits.models import Permit
from .models import *
from .forms import *
import datetime

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
        client: Client = Client.objects.get(pk=self.kwargs['pk'])
        return client

    def get(self, request, *_, **__):
        client: Client = self.get_object() 
        permit: Permit = Permit.objects.filter(client = client).order_by('-pk').first()
        if permit:
            permit_expiration_year: int = permit.expiration_date.year
            current_year: int = datetime.date.today().year
            if permit_expiration_year < current_year:
                messages.warning(request, f"El cliente {client} tiene pendiente de pagos.")
                return redirect(self.success_url)
        messages.success(request, f"El cliente {client} fue liquidado exitosamente.")
        client.active = False
        client.save()
        return redirect(self.success_url)
    

class ClientDownloadLiquidatePDF(MultiGroupRequiredMixin, View):
    groups_required = ["Administrador",]
    success_url = reverse_lazy('clients_list')

    def get(self, _, *__, **___):
        client: Client = Client.objects.get(pk=self.kwargs['pk'])
        permit_file_name = "permiso_liquidacion"
        filename = f"{permit_file_name}.png"
        image_path = os.path.join(settings.MEDIA_ROOT, filename)
        if not os.path.exists(image_path):
            raise Http404("File not found")

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{permit_file_name}.pdf"'
        pdf = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        try:
            image = Image.open(image_path)
            img_width, img_height = image.size
            aspect = img_width / img_height
            new_width = min(width - 40, img_width) 
            new_height = new_width / aspect
            if new_height > height - 40:
                new_height = height - 40
                new_width = new_height * aspect
            pdf.drawImage(image_path, 20, height - new_height - 20, width=new_width, height=new_height)
    
            pdf.drawString(90, 612, f"{datetime.datetime.today().strftime('%Y-%m-%d')}") # todays date
            pdf.drawString(120, 589, f"{client}") # clients name

            pdf.drawString(90, 232, f"{datetime.datetime.today().strftime('%Y-%m-%d')}") # todays date
            pdf.drawString(120, 211, f"{client}") # clients name
            
            pdf.showPage()
            pdf.save()
        except Exception as e:
            return HttpResponse(f"Error processing image: {str(e)}", status=500)

        return response


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