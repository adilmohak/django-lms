from django.urls import path
from .views import *

urlpatterns = [
    path("<int:pk>/quizzes/", quiz_list, name="quiz_index"),
    path("progress/", view=QuizUserProgressView.as_view(), name="quiz_progress"),
    # path('marking/<int:pk>/', view=QuizMarkingList.as_view(), name='quiz_marking'),
    path("marking_list/", view=QuizMarkingList.as_view(), name="quiz_marking"),
    path(
        "marking/<int:pk>/",
        view=QuizMarkingDetail.as_view(),
        name="quiz_marking_detail",
    ),
    path("<int:pk>/<slug>/take/", view=QuizTake.as_view(), name="quiz_take"),
    path('<int:pk>/quiz_add/', QuizCreateView.as_view(), name='quiz_create'),
    path("<int:class_id>/<int:pk>/add/", QuizUpdateView.as_view(), name="quiz_update"),
    path("<int:class_id>/<int:pk>/delete/", quiz_delete, name="quiz_delete"),
    path(
        "mc-question/add/<int:pk>/<int:quiz_id>/",
        MCQuestionCreate.as_view(),
        name="mc_create",
    ),
    # path('mc-question/add/<int:pk>/<quiz_pk>/', MCQuestionCreate.as_view(), name='mc_create'),
]
