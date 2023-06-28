from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("new_honks", views.new_honks, name='new_honks'),
    path("all_honks", views.all_honks, name='all_honks'),
]
