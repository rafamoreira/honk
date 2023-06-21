from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from circus import views

router = routers.DefaultRouter()
router.register(r'honks', views.HonkViewSet)

urlpatterns = [
    path("circus/", include("circus.urls")),
    path('', include(router.urls)),
    path('api', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
