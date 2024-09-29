from modeltranslation.translator import register, TranslationOptions
from .models import Program, Course, Upload, UploadVideo

@register(Program)
class ProgramTranslationOptions(TranslationOptions):
    fields = ('title', 'summary',)
    empty_values=None

@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('title', 'summary',)
    empty_values=None

@register(Upload)
class UploadTranslationOptions(TranslationOptions):
    fields = ('title',)
    empty_values=None

@register(UploadVideo)
class UploadVideoTranslationOptions(TranslationOptions):
    fields = ('title', 'summary',)
    empty_values=None