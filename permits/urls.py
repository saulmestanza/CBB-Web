from django.urls import path
from .views import *

urlpatterns = [
    path('permits/list/', PermitsListView.as_view(), name='permits_list'),
    path('permits/create/', PermitsCreateView.as_view(), name='permits_create'),
    path('permits/download-ficha-inspeccion/', DownloadFichaInspeccionView.as_view(), name='permits_download_inspector_file'),
]
