from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _

from .models import Quiz, Progress, Question, MCQuestion, Choice, Essay_Question, Sitting


class ChoiceInline(admin.TabularInline):
    model = Choice


class QuizAdminForm(forms.ModelForm):

    class Meta:
        model = Quiz
        exclude = []

    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all().select_subclasses(),
        required=False,
        label=_("Questions"),
        widget=FilteredSelectMultiple(
            verbose_name=_("Questions"),
            is_stacked=False))

    def __init__(self, *args, **kwargs):
        super(QuizAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['questions'].initial = self.instance.question_set.all().select_subclasses()

    def save(self, commit=True):
        quiz = super(QuizAdminForm, self).save(commit=False)
        quiz.save()
        quiz.question_set.set(self.cleaned_data['questions'])
        self.save_m2m()
        return quiz


class QuizAdmin(admin.ModelAdmin):
    form = QuizAdminForm

    list_display = ('title', )
    # list_filter = ('category',)
    search_fields = ('description', 'category', )


class MCQuestionAdmin(admin.ModelAdmin):
    list_display = ('content', )
    # list_filter = ('category',)
    fields = ('content', 'figure', 'quiz', 'explanation', 'choice_order')

    search_fields = ('content', 'explanation')
    filter_horizontal = ('quiz',)

    inlines = [ChoiceInline]


class ProgressAdmin(admin.ModelAdmin):
    search_fields = ('user', 'score', )


class EssayQuestionAdmin(admin.ModelAdmin):
    list_display = ('content', )
    # list_filter = ('category',)
    fields = ('content', 'quiz', 'explanation', )
    search_fields = ('content', 'explanation')
    filter_horizontal = ('quiz',)

admin.site.register(Quiz, QuizAdmin)
admin.site.register(MCQuestion, MCQuestionAdmin)
admin.site.register(Progress, ProgressAdmin)
admin.site.register(Essay_Question, EssayQuestionAdmin)
admin.site.register(Sitting)
