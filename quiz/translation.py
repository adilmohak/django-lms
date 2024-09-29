from modeltranslation.translator import register, TranslationOptions
from .models import Quiz, Question, Choice, MCQuestion

@register(Quiz)
class QuizTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)
    empty_values=None

@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ('content', 'explanation',)
    empty_values=None

@register(Choice)
class ChoiceTranslationOptions(TranslationOptions):
    fields = ('choice',)
    empty_values=None

@register(MCQuestion)
class MCQuestionTranslationOptions(TranslationOptions):
    pass