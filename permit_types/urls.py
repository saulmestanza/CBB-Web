from django.urls import path
from permit_types.views import * 

urlpatterns = [
    path("permit-types/list/", PermitTypesListView.as_view(), name="permit_types_list"),
    path("permit-types/<int:pk>/delete/", PermitTypesDeleteView.as_view(), name="permit_types_delete"),
    path("permit-types/create/", PermitTypesCreateView.as_view(), name="permit_types_create"),
    path("permit-types/<int:pk>/edit/", PermitTypesUpdateView.as_view(), name="permit_types_edit"),
]