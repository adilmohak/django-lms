from . import views

from django.urls import path

app_name = "accounts-api"

urlpatterns = [
    path('', views.UserListAPIView.as_view(), name="users-api"),
]