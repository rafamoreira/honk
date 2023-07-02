from django.urls import path
from circus import web_views
from circus import api_views

urlpatterns = [
    path("", web_views.home, name='home'),
    path("new_honks", web_views.new_honks, name='new_honks'),
    path("all_honks", web_views.all_honks, name='all_honks'),
    path("new_honk", web_views.new_honk, name='new_honk'),
    path("honks/", api_views.honk_list),
    path("honks/<int:pk>/", api_views.honk_detail),
    path("users/", api_views.UserList.as_view()),
    path("users/<int:pk>/", api_views.UserDetail.as_view()),
]
