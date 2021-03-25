from django.conf.urls import url

from .views import SearchView

urlpatterns = [
    url(r'^$', SearchView.as_view(), name='query'),
]

