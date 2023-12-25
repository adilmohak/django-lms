from django.urls import path
from . import views

app_name = "accounts-api"

urlpatterns = [
    path("", views.UserListAPIView.as_view(), name="users-api"),
]
