from django.urls import path
from . import views

urlpatterns = [
    path("honk", views.honk, name='honk'),
]
