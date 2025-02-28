from django.urls import path
from authentication.views import * 

urlpatterns = [
    path("login/", LogInView.as_view(), name="login"),
    path("logout/", LogOutView.as_view(), name="logout"),
]