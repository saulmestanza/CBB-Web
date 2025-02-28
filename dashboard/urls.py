from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from dashboard.views import * 

urlpatterns = [
    path("login/", LogInView.as_view(), name="login"),
    path("logout/", LogOutView.as_view(), name="logout"),
    path("users/", UsersListView.as_view(), name="users_list")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)