from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Session, Semester, NewsAndEvents
from modeltranslation.admin import TranslationAdmin

class NewsAndEventsAdmin(TranslationAdmin):
    pass

admin.site.register(Semester)
admin.site.register(Session)
admin.site.register(NewsAndEvents, NewsAndEventsAdmin)
