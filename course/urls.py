from django.conf.urls import url
from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, 
    PasswordResetCompleteView, LoginView, LogoutView
)
# from .views import (
#     program_view, program_detail, program_add, program_edit, program_delete, 
#     course_single, course_add, course_edit, course_delete, 
#     CourseAllocationFormView, course_allocation_view, edit_allocated_course, deallocate_course, 
#     handle_file_upload, handle_file_edit, handle_file_delete, 
#     course_registration, course_drop, user_course_list
# )
from .views import *


urlpatterns = [
    # Program urls
    url(r'^$', program_view, name='programs'),
    url(r'^(?P<pk>\d+)/detail/$', program_detail, name='program_detail'),
    url(r'^add/$', program_add, name='add_program'),
    url(r'^(?P<pk>\d+)/edit/$', program_edit, name='edit_program'),
    url(r'^(?P<pk>\d+)/delete/$', program_delete, name='program_delete'),

    # Course urls
    url(r'^course/(?P<slug>[\w-]+)/detail/$', course_single, name='course_detail'),
    url(r'^(?P<pk>\d+)/course/add/$', course_add, name='course_add'),
    url(r'^course/(?P<slug>[\w-]+)/edit/$', course_edit, name='edit_course'),
    url(r'^course/delete/(?P<slug>[\w-]+)/$', course_delete, name='delete_course'),

    # CourseAllocation urls
    url(r'^course/assign/$', CourseAllocationFormView.as_view(), name='course_allocation'),
    url(r'^course/allocated/$', course_allocation_view, name='course_allocation_view'),
    url(r'^allocated_course/(?P<pk>\d+)/edit/$', edit_allocated_course, name='edit_allocated_course'),
    url(r'^course/(?P<pk>\d+)/deallocate/$', deallocate_course, name='course_deallocate'),

    # File uploads urls
    url(r'^course/(?P<slug>[\w-]+)/documentations/upload/$', handle_file_upload, name='upload_file_view'),
    url(r'^course/(?P<slug>[\w-]+)/documentations/(?P<file_id>\d+)/edit/$', handle_file_edit, name='upload_file_edit'),
    url(r'^course/(?P<slug>[\w-]+)/documentations/(?P<file_id>\d+)/delete/$', handle_file_delete, name='upload_file_delete'),

    # Video uploads urls
    url(r'^course/(?P<slug>[\w-]+)/video_tutorials/upload/$', handle_video_upload, name='upload_video'),
    url(r'^course/(?P<slug>[\w-]+)/video_tutorials/(?P<video_slug>[\w-]+)/detail/$', handle_video_single, name='video_single'),
    url(r'^course/(?P<slug>[\w-]+)/video_tutorials/(?P<video_slug>[\w-]+)/edit/$', handle_video_edit, name='upload_video_edit'),
    url(r'^course/(?P<slug>[\w-]+)/video_tutorials/(?P<video_slug>[\w-]+)/delete/$', handle_video_delete, name='upload_video_delete'),

    # course registration
    url(r'^course/registration/$', course_registration, name='course_registration'),
    url(r'^course/drop/$', course_drop, name='course_drop'),
    
    url(r'^my_courses/$', user_course_list, name="user_course_list"),
]
