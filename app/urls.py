from django.conf.urls import url
from django.urls import path

from .views import (
    home_view, post_add, edit_post, delete_post, 
    session_list_view, session_add_view, session_update_view, session_delete_view, 
    semester_list_view, semester_add_view, semester_update_view, semester_delete_view,
    dashboard_view
) 


urlpatterns = [
    # Accounts url
    url(r'^$', home_view, name='home'),
    url(r'^add_item/$', post_add, name='add_item'),
    url(r'^item/(?P<pk>\d+)/edit/$', edit_post, name='edit_post'),
    url(r'^item/(?P<pk>\d+)/delete/$', delete_post, name='delete_post'),

    url(r'^session/$', session_list_view, name="session_list"),
    url(r'^session/add/$', session_add_view, name="add_session"),
    url(r'^session/(?P<pk>\d+)/edit/$', session_update_view, name="edit_session"),
    url(r'^session/(?P<pk>\d+)/delete/$', session_delete_view, name="delete_session"),

    url(r'^semester/$', semester_list_view, name="semester_list"),
    url(r'^semester/add/$', semester_add_view, name="add_semester"),
    url(r'^semester/(?P<pk>\d+)/edit/$', semester_update_view, name="edit_semester"),
    url(r'^semester/(?P<pk>\d+)/delete/$', semester_delete_view, name="delete_semester"),

    url(r'^dashboard/$', dashboard_view, name="dashboard"),
]
