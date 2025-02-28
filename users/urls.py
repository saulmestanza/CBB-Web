from django.urls import path
from users.views import * 

urlpatterns = [
    path("users/", UsersListView.as_view(), name="users_list"),
    path('users/create/', UsersCreateView.as_view(), name='users_create'),
    path('users/<int:pk>/edit/', UsersUpdateView.as_view(), name='users_edit'),
    path('users/<int:pk>/delete/', UsersDeleteView.as_view(), name='users_delete'),
    path('users/<int:pk>/reset-password/', UserPasswordResetView.as_view(), name='users_reset_password'),
]