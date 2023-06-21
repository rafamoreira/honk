from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from circus.models import Honk
from circus.serializers import HonkSerializer


@login_required
def honk(request):
    return render(request, 'circus/honk.html')


class HonkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows honks to be viewed or edited.
    """
    queryset = Honk.objects.all()
    serializer_class = HonkSerializer
    # permission_classes = [permissions.IsAuthenticated]
