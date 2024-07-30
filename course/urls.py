from django.urls import path
from .views import *


urlpatterns = [
    # Program urls
    path("", ProgramFilterView.as_view(), name="programs"),
    path("<int:pk>/detail/", program_detail, name="program_detail"),
    path("add/", program_add, name="add_program"),
    path("add_timeslot", add_timeslot, name="add_timeslot"),
    path("<int:pk>/edit/", program_edit, name="edit_program"),
    path("<int:pk>/delete/", program_delete, name="program_delete"),
    ###############################################################
    # Course urls
    ###############################################################
    path("course/<slug>/detail/", course_single, name="course_detail"),
    path("<int:pk>/course/add/", course_add, name="course_add"),
    path("course/<slug>/add_class", class_add, name = "course_add_class"),
    path("course/<slug>/edit/", course_edit, name="edit_course"),
    path("course/delete/<slug>/", course_delete, name="delete_course"),
    # CourseAllocation urls
    path(
        "course/assign/", CourseAllocationFormView.as_view(), name="course_allocation"
    ),
    path(
        "course/allocated/",
        CourseAllocationFilterView.as_view(),
        name="course_allocation_view",
    ),
    path(
        "allocated_course/<int:pk>/edit/",
        edit_allocated_course,
        name="edit_allocated_course",
    ),
    path("course/<int:pk>/deallocate/", deallocate_course, name="course_deallocate"),
    # course registration
    path("course/registration/", course_registration, name="course_registration"),
    path("course/drop/", course_drop, name="course_drop"),
    path("my_courses/", user_course_list, name="user_course_list"),
    ###############################################################
    # Class urls
    ###############################################################
    path('get_lecturers_by_course/<int:course_id>/', get_lecturers_by_course, name='get_lecturers_by_course'),
    path("class_assign", ClassAddView.as_view(), name="class_assign"),
    path("class_list", ClassAllocationFilterView.as_view(), name="class_list"),
    path("class/<int:pk>/detail/", class_single, name="class_detail"),
    path("class/<int:pk>/edit", edit_allocated_class, name = "class_edit"),
    path("class/<int:pk>/delete", deallocate_class, name = "class_delete"),
    ###############################################################
    # File upload
    ###############################################################
    path(
        "class/<int:pk>/documentations/upload/",
        handle_file_upload,
        name="upload_file_view",
    ),
    path(
        "class/<int:pk>/documentations/<int:file_id>/edit/",
        handle_file_edit,
        name="upload_file_edit",
    ),
    path(
        "class/<int:pk>/documentations/<int:file_id>/delete/",
        handle_file_delete,
        name="upload_file_delete",
    ),
    # Video uploads urls
    path(
        "class/<int:pk>/video_tutorials/upload/",
        handle_video_upload,
        name="upload_video",
    ),
    path(
        "class/<int:pk>/video_tutorials/<video_slug>/detail/",
        handle_video_single,
        name="video_single",
    ),
    path(
        "class/<int:pk>/video_tutorials/<video_slug>/edit/",
        handle_video_edit,
        name="upload_video_edit",
    ),
    path(
        "class/<int:pk>/video_tutorials/<video_slug>/delete/",
        handle_video_delete,
        name="upload_video_delete",
    ),
]
