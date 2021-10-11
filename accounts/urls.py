from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, 
    PasswordResetCompleteView, LoginView, LogoutView
    )
from .views import (
        profile, profile_single, admin_panel, 
        profile_update, change_password, 
        LecturerListView, StudentListView, 
        staff_add_view, edit_staff, 
        delete_staff, student_add_view, 
        edit_student, delete_student, ParentAdd, validate_username, register
    )
from .forms import EmailValidationOnForgotPassword


urlpatterns = [
    path('', include('django.contrib.auth.urls')),

    url(r'^admin_panel/$', admin_panel, name='admin_panel'),

    url(r'^profile/$', profile, name='profile'),
    url(r'^profile/(?P<id>\d+)/detail/$', profile_single, name='profile_single'),
    url(r'^setting/$', profile_update, name='edit_profile'),
    url(r'^change_password/$', change_password, name='change_password'),

    url(r'^lecturers/$', LecturerListView.as_view(), name='lecturer_list'),
    url(r'^lecturer/add/$', staff_add_view, name='add_lecturer'),
    url(r'^staff/(?P<pk>\d+)/edit/$', edit_staff, name='staff_edit'),
    url(r'^lecturers/(?P<pk>\d+)/delete/$', delete_staff, name='lecturer_delete'),

    url(r'^students/$', StudentListView.as_view(), name='student_list'),
    url(r'^student/add/$', student_add_view, name='add_student'),
    url(r'^student/(?P<pk>\d+)/edit/$', edit_student, name='student_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$', delete_student, name='student_delete'),

    url(r'^parents/add/$', ParentAdd.as_view(), name='add_parent'),

    url(r'^ajax/validate-username/$', validate_username, name='validate_username'),

    url(r'^register/$', register, name='register'),

    # url(r'^add-student/$', StudentAddView.as_view(), name='add_student'),

    # url(r'^programs/course/delete/(?P<pk>\d+)/$', course_delete, name='delete_course'),

    # Setting urls
    # url(r'^profile/(?P<pk>\d+)/edit/$', profileUpdateView, name='edit_profile'),
    # url(r'^profile/(?P<pk>\d+)/change-password/$', changePasswordView, name='change_password'),

    # ################################################################
    # url(r'^login/$', LoginView.as_view(), name='login'),
    # url(r'^logout/$', LogoutView.as_view(), name='logout', kwargs={'next_page': '/'}),

    # url(r'^password-reset/$', PasswordResetView.as_view(
    #     form_class=EmailValidationOnForgotPassword,
    #     template_name='registration/password_reset.html'
    # ),
    #      name='password_reset'),
    # url(r'^password-reset/done/$', PasswordResetDoneView.as_view(
    #     template_name='registration/password_reset_done.html'
    # ),
    #      name='password_reset_done'),
    # url(r'^password-reset-confirm/<uidb64>/<token>/$', PasswordResetConfirmView.as_view(
    #     template_name='registration/password_reset_confirm.html'
    # ),
    #      name='password_reset_confirm'),
    # url(r'^password-reset-complete/$', PasswordResetCompleteView.as_view(
    #     template_name='registration/password_reset_complete.html'
    # ),
    #      name='password_reset_complete')
    # ################################################################
]
