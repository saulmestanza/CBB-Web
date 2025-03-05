import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.views import View
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
from utils.mixins import MultiGroupRequiredMixin
from .forms import *
from .models import Permit


class PermitsListView(MultiGroupRequiredMixin, ListView):
    model = Permit
    template_name = 'permits/permits_list.html'
    context_object_name = 'permits' 
    login_url = ''
    redirect_field_name = 'next' 
    groups_required = ["Administrador",]
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset().all().order_by('permit_code').order_by('permit_type')
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(permit_code__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        user_group_names = self.request.user.groups.values_list('name', flat=True)
        context['user_group_names'] = user_group_names
        return context
    

class PermitsCreateView(MultiGroupRequiredMixin, CreateView):
    model = Permit
    form_class = PermitForm 
    groups_required = ["Administrador",]
    template_name = 'permits/permits_form.html'
    success_url = reverse_lazy('permits_list') 

    def form_valid(self, form):
        return super().form_valid(form)


class DownloadFichaInspeccionView(View):
    def get(self, request):
        filename = "ficha_inspeccion.png"
        # Get the image path
        image_path = os.path.join(settings.MEDIA_ROOT, filename)

        # Check if the file exists
        if not os.path.exists(image_path):
            raise Http404("File not found")

        # Create a response with PDF content type
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'

        # Create PDF
        pdf = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        try:
            # Open image
            image = Image.open(image_path)
            img_width, img_height = image.size

            # Scale image to fit PDF page
            aspect = img_width / img_height
            new_width = min(width - 40, img_width)  # Leave some margin
            new_height = new_width / aspect

            if new_height > height - 40:
                new_height = height - 40
                new_width = new_height * aspect

            # Draw image onto PDF
            pdf.drawImage(image_path, 20, height - new_height - 20, width=new_width, height=new_height)
            pdf.showPage()
            pdf.save()
        except Exception as e:
            return HttpResponse(f"Error processing image: {str(e)}", status=500)

        return response
