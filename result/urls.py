from django.conf.urls import url
from django.urls import path
from .views import (
    add_score, add_score_for, grade_result, assessment_result, 
    course_registration_form, result_sheet_pdf_view
)


urlpatterns = [
    url(r'^manage-score/$', add_score, name='add_score'),
    url(r'^manage-score/(?P<id>\d+)/$', add_score_for, name='add_score_for'),
    
    url(r'^grade/$', grade_result, name="grade_results"),
    url(r'^assessment/$', assessment_result, name="ass_results"),

	url(r'^result/print/(?P<id>\d+)/$', result_sheet_pdf_view, name='result_sheet_pdf_view'),
	url(r'^registration/form/$', course_registration_form, name='course_registration_form'),
]
