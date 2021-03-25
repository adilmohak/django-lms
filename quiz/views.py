import random

from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, TemplateView, FormView, CreateView, FormView, DeleteView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect

from accounts.decorators import student_required, lecturer_required
from .models import *
from .forms import *


@method_decorator([login_required, lecturer_required], name='dispatch')
class QuizCreateView(CreateView):
    model = Quiz
    form_class = QuizAddForm

    def get_context_data(self, *args, **kwargs):
        context = super(QuizCreateView, self).get_context_data(**kwargs)
        context['course'] = Course.objects.get(slug=self.kwargs['slug'])
        if self.request.POST:
            context['form'] = QuizAddForm(self.request.POST)
            # context['quiz'] = self.request.POST.get('quiz')
        else:
            context['form'] = QuizAddForm(initial={'course': Course.objects.get(slug=self.kwargs['slug'])})
        return context

    def form_valid(self, form, **kwargs):
        context = self.get_context_data()
        form = context['form']
        with transaction.atomic():
            self.object = form.save()
            if form.is_valid():
                form.instance = self.object
                form.save()
                return redirect('mc_create', slug=self.kwargs['slug'], quiz_id=form.instance.id)
        return super(QuizCreateView, self).form_invalid(form)


@method_decorator([login_required, lecturer_required], name='dispatch')
class QuizUpdateView(UpdateView):
    model = Quiz
    form_class = QuizAddForm

    def get_context_data(self, *args, **kwargs):
        context = super(QuizUpdateView, self).get_context_data(**kwargs)
        context['course'] = Course.objects.get(slug=self.kwargs['slug'])
        quiz = Quiz.objects.get(pk=self.kwargs['pk'])
        if self.request.POST:
            context['form'] = QuizAddForm(self.request.POST, instance=quiz)
        else:
            context['form'] = QuizAddForm(instance=quiz)
        return context

    def form_valid(self, form, **kwargs):
        context = self.get_context_data()
        course = context['course']
        form = context['form']
        with transaction.atomic():
            self.object = form.save()
            if form.is_valid():
                form.instance = self.object
                form.save()
                return redirect('quiz_index', course.slug)
        return super(QuizUpdateView, self).form_invalid(form)


@login_required
@lecturer_required
def quiz_delete(request, slug, pk):
    quiz = Quiz.objects.get(pk=pk)
    course = Course.objects.get(slug=slug)
    quiz.delete()
    messages.success(request, f'successfuly deleted.')
    return redirect('quiz_index', quiz.course.slug)


@method_decorator([login_required, lecturer_required], name='dispatch')
class MCQuestionCreate(CreateView):
    model = MCQuestion
    form_class = MCQuestionForm

    def get_context_data(self, **kwargs):
        context = super(MCQuestionCreate, self).get_context_data(**kwargs)
        context['course'] = Course.objects.get(slug=self.kwargs['slug'])
        context['quiz_obj'] = Quiz.objects.get(id=self.kwargs['quiz_id'])
        context['quizQuestions'] = Question.objects.filter(quiz=self.kwargs['quiz_id']).count()
        if self.request.POST:
            context['form'] = MCQuestionForm(self.request.POST)
            context['formset'] = MCQuestionFormSet(self.request.POST)
        else:
            context['form'] = MCQuestionForm(initial={'quiz': self.kwargs['quiz_id']})
            context['formset'] = MCQuestionFormSet()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        course = context['course']
        with transaction.atomic():
            form.instance.question = self.request.POST.get('content')
            self.object = form.save()
            if formset.is_valid():
                formset.instance = self.object
                formset.save()
                if "another" in self.request.POST:
                    return redirect('mc_create', slug=self.kwargs['slug'], quiz_id=self.kwargs['quiz_id'])
                return redirect('quiz_index', course.slug)
        return super(MCQuestionCreate, self).form_invalid(form)


@login_required
def quiz_list(request, slug):
    quizzes = Quiz.objects.filter(course__slug = slug).order_by('-timestamp')
    course = Course.objects.get(slug = slug)
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes, 'course': course})
    # return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})


@method_decorator([login_required, lecturer_required], name='dispatch')
class QuizMarkerMixin(object):
    @method_decorator(login_required)
    # @method_decorator(permission_required('quiz.view_sittings'))
    def dispatch(self, *args, **kwargs):
        return super(QuizMarkerMixin, self).dispatch(*args, **kwargs)


# @method_decorator([login_required, lecturer_required], name='get_queryset')
class SittingFilterTitleMixin(object):
    def get_queryset(self):
        queryset = super(SittingFilterTitleMixin, self).get_queryset()
        quiz_filter = self.request.GET.get('quiz_filter')
        if quiz_filter:
            queryset = queryset.filter(quiz__title__icontains=quiz_filter)

        return queryset


@method_decorator([login_required], name='dispatch')
class QuizUserProgressView(TemplateView):
    template_name = 'progress.html'

    def dispatch(self, request, *args, **kwargs):
        return super(QuizUserProgressView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(QuizUserProgressView, self).get_context_data(**kwargs)
        progress, c = Progress.objects.get_or_create(user=self.request.user)
        context['cat_scores'] = progress.list_all_cat_scores
        context['exams'] = progress.show_exams()
        context['exams_counter'] = progress.show_exams().count()
        return context

from result.models import TakenCourse

@method_decorator([login_required, lecturer_required], name='dispatch')
class QuizMarkingList(QuizMarkerMixin, SittingFilterTitleMixin, ListView):
    model = Sitting
    # def get_context_data(self, **kwargs):
    #     context = super(QuizMarkingList, self).get_context_data(**kwargs)
    #     context['queryset_counter'] = super(QuizMarkingList, self).get_queryset().filter(complete=True).filter(course__allocated_course__lecturer__pk=self.request.user.id).count()
    #     context['marking_list'] = super(QuizMarkingList, self).get_queryset().filter(complete=True).filter(course__allocated_course__lecturer__pk=self.request.user.id)
    #     return context
    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = super(QuizMarkingList, self).get_queryset().filter(complete=True)
        else:
            queryset = super(QuizMarkingList, self).get_queryset().filter(quiz__course__allocated_course__lecturer__pk=self.request.user.id).filter(complete=True)

        # search by user
        user_filter = self.request.GET.get('user_filter')
        if user_filter:
            queryset = queryset.filter(user__username__icontains=user_filter)
            
        return queryset


@method_decorator([login_required, lecturer_required], name='dispatch')
class QuizMarkingDetail(QuizMarkerMixin, DetailView):
    model = Sitting

    def post(self, request, *args, **kwargs):
        sitting = self.get_object()

        q_to_toggle = request.POST.get('qid', None)
        if q_to_toggle:
            q = Question.objects.get_subclass(id=int(q_to_toggle))
            if int(q_to_toggle) in sitting.get_incorrect_questions:
                sitting.remove_incorrect_question(q)
            else:
                sitting.add_incorrect_question(q)

        return self.get(request)

    def get_context_data(self, **kwargs):
        context = super(QuizMarkingDetail, self).get_context_data(**kwargs)
        context['questions'] = context['sitting'].get_questions(with_answers=True)
        return context


# @method_decorator([login_required, student_required], name='dispatch')
@method_decorator([login_required], name='dispatch')
class QuizTake(FormView):
    form_class = QuestionForm
    template_name = 'question.html'
    result_template_name = 'result.html'
    # single_complete_template_name = 'single_complete.html'

    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, slug=self.kwargs['slug'])
        self.course = get_object_or_404(Course, pk=self.kwargs['pk'])
        quizQuestions = Question.objects.filter(quiz=self.quiz).count()
        course = get_object_or_404(Course, pk=self.kwargs['pk'])

        if quizQuestions <= 0:
            messages.warning(request, f'Question set of the quiz is empty. try later!')
            return redirect('quiz_index', self.course.slug)

        if self.quiz.draft and not request.user.has_perm('quiz.change_quiz'):
            raise PermissionDenied

        self.sitting = Sitting.objects.user_sitting(request.user, self.quiz, self.course)

        if self.sitting is False:
            # return render(request, self.single_complete_template_name)
            messages.info(request, f'You have already sat this exam and only one sitting is permitted')
            return redirect('quiz_index', self.course.slug)

        return super(QuizTake, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        self.question = self.sitting.get_first_question()
        self.progress = self.sitting.progress()

        if self.question.__class__ is Essay_Question:
            form_class = EssayForm
        else:
            form_class = self.form_class

        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(QuizTake, self).get_form_kwargs()

        return dict(kwargs, question=self.question)

    def form_valid(self, form):
        self.form_valid_user(form)
        if self.sitting.get_first_question() is False:
            return self.final_result_user()

        self.request.POST = {}

        return super(QuizTake, self).get(self, self.request)

    def get_context_data(self, **kwargs):
        context = super(QuizTake, self).get_context_data(**kwargs)
        context['question'] = self.question
        context['quiz'] = self.quiz
        context['course'] = get_object_or_404(Course, pk=self.kwargs['pk'])
        if hasattr(self, 'previous'):
            context['previous'] = self.previous
        if hasattr(self, 'progress'):
            context['progress'] = self.progress
        return context

    def form_valid_user(self, form):
        progress, c = Progress.objects.get_or_create(user=self.request.user)
        guess = form.cleaned_data['answers']
        is_correct = self.question.check_if_correct(guess)

        if is_correct is True:
            self.sitting.add_to_score(1)
            progress.update_score(self.question, 1, 1)
        else:
            self.sitting.add_incorrect_question(self.question)
            progress.update_score(self.question, 0, 1)

        if self.quiz.answers_at_end is not True:
            self.previous = {
                'previous_answer': guess,
                'previous_outcome': is_correct,
                'previous_question': self.question,
                'answers': self.question.get_choices(),
                'question_type': {self.question.__class__.__name__: True}
            }
        else:
            self.previous = {}

        self.sitting.add_user_answer(self.question, guess)
        self.sitting.remove_first_question()

    def final_result_user(self):
        results = {
            'course': get_object_or_404(Course, pk=self.kwargs['pk']),
            'quiz': self.quiz,
            'score': self.sitting.get_current_score,
            'max_score': self.sitting.get_max_score,
            'percent': self.sitting.get_percent_correct,
            'sitting': self.sitting,
            'previous': self.previous,
            'course': get_object_or_404(Course, pk=self.kwargs['pk'])
        }

        self.sitting.mark_quiz_complete()

        if self.quiz.answers_at_end:
            results['questions'] = self.sitting.get_questions(with_answers=True)
            results['incorrect_questions'] = self.sitting.get_incorrect_questions

        if self.quiz.exam_paper is False or self.request.user.is_superuser or self.request.user.is_lecturer :
            self.sitting.delete()

        return render(self.request, self.result_template_name, results)
