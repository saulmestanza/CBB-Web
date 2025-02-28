from django.urls import path
from dashboard.views import * 

urlpatterns = [
    path("users/", UsersListView.as_view(), name="users_list")
]