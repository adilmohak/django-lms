from rest_framework import generics
from django.contrib.auth.views import get_user_model

from .serializers import UserSerializer

User = get_user_model()


class UserListAPIView(generics.ListAPIView):
    lookup_field = 'id'
    serializer_class = UserSerializer

    def get_queryset(self):
        qs = User.objects.all()
        q = self.request.GET.get('q')
        if q is not None:
            qs = qs.filter(username__iexact=q)
        return qs


class UserDetailView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = User.objects.all()
    model = User
