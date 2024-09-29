from modeltranslation.translator import register, TranslationOptions
from .models import NewsAndEvents, ActivityLog

@register(NewsAndEvents)
class NewsAndEventsTranslationOptions(TranslationOptions):
    fields = ('title', 'summary',)
    empty_values=None

