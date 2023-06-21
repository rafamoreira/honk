from django.urls import path
from . import views

urlpatterns = [
    path("my_honks", views.my_honks, name='my_honks'),
]
