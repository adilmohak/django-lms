from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from django.conf.urls import handler404, handler500, handler400
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^', include('app.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^programs/', include('course.urls')),
    url(r'^result/', include('result.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^quiz/', include('quiz.urls')),

    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = 'app.views.handler404'
# handler500 = 'app.views.handler500'
# handler400 = 'app.views.handler400'
