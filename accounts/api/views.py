from rest_framework import generics
from django.contrib.auth import get_user_model

from .serializers import UserSerializer


class UserListAPIView(generics.ListAPIView):
    lookup_field = "id"
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = get_user_model().objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            queryset = queryset.filter(username__iexact=q)
        return queryset


class UserDetailView(generics.RetrieveAPIView):
    User = get_user_model()
    lookup_field = "id"
    queryset = User.objects.all()
    model = User
