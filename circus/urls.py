from django.urls import path
from circus import views

urlpatterns = [
    path("", views.home, name='home'),
    path("new_honks", views.new_honks, name='new_honks'),
    path("all_honks", views.all_honks, name='all_honks'),
    path("honks/", views.honk_list),
    path("honks/<int:pk>/", views.honk_detail),
    path("users/", views.UserList.as_view()),
    path("users/<int:pk>/", views.UserDetail.as_view()),
]
