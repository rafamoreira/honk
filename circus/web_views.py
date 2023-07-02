"""
circus views
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from circus.models import Honk


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
