from django import forms
from django.forms.widgets import RadioSelect, Textarea
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _
from django.db import transaction

from django.forms.models import inlineformset_factory

from accounts.models import User
from .models import Question, Quiz, MCQuestion, Choice


class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        choice_list = [x for x in question.get_choices_list()]
        self.fields["answers"] = forms.ChoiceField(choices=choice_list, widget=RadioSelect)


class EssayForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(EssayForm, self).__init__(*args, **kwargs)
        self.fields["answers"] = forms.CharField(
            widget=Textarea(attrs={'style': 'width:100%'}))


class QuizAddForm(forms.ModelForm):

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
        super(QuizAddForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['questions'].initial = self.instance.question_set.all().select_subclasses()

    def save(self, commit=True):
        quiz = super(QuizAddForm, self).save(commit=False)
        quiz.save()
        quiz.question_set.set(self.cleaned_data['questions'])
        self.save_m2m()
        return quiz


class MCQuestionForm(forms.ModelForm):

    class Meta:
        model = MCQuestion
        exclude = ()


MCQuestionFormSet = inlineformset_factory(
    MCQuestion, Choice, form=MCQuestionForm, fields=['choice', 'correct'], can_delete=True, extra=5
)
