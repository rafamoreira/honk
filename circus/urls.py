from django.urls import path
from circus import views
from circus import api_views

urlpatterns = [
    path("", views.home, name='home'),
    path("new_honks", views.new_honks, name='new_honks'),
    path("all_honks", views.all_honks, name='all_honks'),
    path("honks/", api_views.honk_list),
    path("honks/<int:pk>/", api_views.honk_detail),
    path("users/", api_views.UserList.as_view()),
    path("users/<int:pk>/", api_views.UserDetail.as_view()),
]
