from django.urls import path
from circus import web_views
from circus import api_views

urlpatterns = [
    path("", web_views.home, name='home'),
    path("honks/", web_views.all_honks, name='all_honks'),
    path("honks/new", web_views.new_honk, name='new_honk'),
    path("honks/unread", web_views.unread_honks, name='unread_honks'),
    path("honks/sent", web_views.sent_honks, name='sent_honks'),
    path("honks/<int:pk>/read", web_views.read_honk, name='read_honk'),
    path("magic_word", web_views.magic_word, name='magic_word'),

    path("honks/", api_views.honk_list),
    path("honks/<int:pk>/", api_views.honk_detail),
    path("users/", api_views.UserList.as_view()),
    path("users/<int:pk>/", api_views.UserDetail.as_view()),
]
