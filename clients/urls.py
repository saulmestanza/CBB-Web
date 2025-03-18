from django.urls import path
from .views import * 

urlpatterns = [
    path("clients/list/", ClientsListView.as_view(), name="clients_list"),
    path("clients/<int:pk>/delete/", ClientsDeleteView.as_view(), name="clients_delete"),
    path("clients/create/", ClientsCreateView.as_view(), name="clients_create"),
    path("clients/<int:pk>/edit/", ClientsUpdateView.as_view(), name="clients_edit"),
    path("clients/<int:pk>/liquidate/", ClientDownloadLiquidatePDF.as_view(), name="clients_download_liquidate_pdf"),
]