from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from circus.models import Honk
from circus.serializers import HonkSerializer


@login_required
def my_honks(request):
    """
    /circus/my_honks
    """
    context = {
        'honks': Honk.get_honks(honked_id=request.user.id),
    }
    return render(request, 'circus/honk.html', context)


class HonkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows honks to be viewed or edited.
    """
    queryset = Honk.objects.all()
    serializer_class = HonkSerializer
    # permission_classes = [permissions.IsAuthenticated]
