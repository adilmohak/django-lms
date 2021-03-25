from django.conf.urls import url

from .views import *

urlpatterns = [

    url(r'^(?P<slug>[\w-]+)/quizzes/$', quiz_list, name='quiz_index'),

    url(r'^progress/$', view=QuizUserProgressView.as_view(), name='quiz_progress'),

    # url(r'^marking/(?P<pk>[\d.]+)/$', view=QuizMarkingList.as_view(), name='quiz_marking'),
    url(r'^marking_list/$', view=QuizMarkingList.as_view(), name='quiz_marking'),

    url(r'^marking/(?P<pk>[\d.]+)/$', view=QuizMarkingDetail.as_view(), name='quiz_marking_detail'),

    url(r'^(?P<pk>[\d.]+)/(?P<slug>[\w-]+)/take/$', view=QuizTake.as_view(), name='quiz_take'),

    url(r'^(?P<slug>[\w-]+)/quiz_add/$', QuizCreateView.as_view(), name='quiz_create'),
    url(r'^(?P<slug>[\w-]+)/(?P<pk>[\d.]+)/add/$', QuizUpdateView.as_view(), name='quiz_update'),
    url(r'^(?P<slug>[\w-]+)/(?P<pk>[\d.]+)/delete/$', quiz_delete, name='quiz_delete'),
    url(r'^mc-question/add/(?P<slug>[\w-]+)/(?P<quiz_id>[\d.]+)/$', MCQuestionCreate.as_view(), name='mc_create'),
    # url(r'^mc-question/add/(?P<pk>[\d.]+)/(?P<quiz_pk>[\d.]+)/$', MCQuestionCreate.as_view(), name='mc_create'),
]
