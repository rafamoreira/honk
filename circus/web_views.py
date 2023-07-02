"""
circus views
"""
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from circus.forms import NewHonk
from circus.models import Honk


HONKS_LIST = 'circus/honks.html'


@login_required
def home(request):
    """
    /
    """
    return all_honks(request)


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
def new_honk(request):
    """
    /new_honk
    """
    if request.method == 'POST':
        form = NewHonk(request.POST, honker_id=request.user.id)
        if form.is_valid():
            honk = form.save(commit=False)
            honk.honker = request.user
            honk.save()
            rendered_honk = Honk.get_honk(honk.id)
            return render(
                request,
                'circus/created_honk.html',
                {'honk': rendered_honk},
            )
        return render(request, 'circus/new_honk.html')
    else:
        form = NewHonk(honker_id=request.user.id)
    return render(request, 'circus/new_honk.html', {'form': form})


@login_required
def unread_honks(request):
    """
    /new_honks
    """
    context = {
        'honks': Honk.get_unread_honks(
            honked_id=request.user.id,
        ),
    }
    return render(request, HONKS_LIST, context)


@login_required
def sent_honks(request):
    """
    /sent_honks
    """
    context = {
        'honks': Honk.get_sent_honks(honker_id=request.user.id),
    }
    return render(request, "circus/sent_honks.html", context)


@login_required
def read_honk(request, pk):
    """
    /honks/<int:pk>/read
    """
    honk = Honk.objects.get(id=pk)
    if honk.honked_id != request.user.id:
        return HttpResponseRedirect(reverse('circus:magic_word'))

    honk.mark_as_seen()
    return HttpResponseRedirect(reverse('circus:unread_honks'))


def magic_word(request):
    """
    /magic_word
    """
    return render(request, 'circus/magic_word.html')
