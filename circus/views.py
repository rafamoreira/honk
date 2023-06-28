from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from circus.models import Honk
from circus.serializers import HonkSerializer

HONKS_LIST = 'circus/honks.html'


@login_required
def all_honks(request):
    """
    /all_honks
    """
    context = {
        'honks': Honk.get_honks(honked_id=request.user.id),
    }
    return render(request, HONKS_LIST, context)


@login_required
def new_honks(request):
    """
    /new_honks
    """
    context = {
        'honks': Honk.get_honks(
            honked_id=request.user.id, only_unseen=True, mark_as_seen=True
        ),
    }
    return render(request, HONKS_LIST, context)


@login_required
def sent_honks(request):
    """
    /sent_honks
    """
    context = {
        'honks': Honk.get_honks(honker_id=request.user.id),
    }
    return render(request, HONKS_LIST, context)


@login_required
def home(request):
    """
    /
    """
    return all_honks(request)


# class HonkViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows honks to be viewed or edited.
#     """
#     queryset = Honk.objects.all()
#     serializer_class = HonkSerializer
#     # permission_classes = [permissions.IsAuthenticated]
