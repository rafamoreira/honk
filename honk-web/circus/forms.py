from django import forms
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from circus.models import Clown, Honk


class ClownChoiceField(forms.ModelChoiceField):
    """
    Custom field for choosing a clown
    """
    def label_from_instance(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" width="100" height="100" />'
        )


class NewHonk(forms.ModelForm):
    """
    Form for creating a new honk
    """
    honked = forms.ModelChoiceField(
        queryset=None,
        empty_label="Choose someone to honk",
    )
    clown = ClownChoiceField(
        queryset=Clown.objects.all(),
        empty_label="Choose a clown",
        widget=forms.RadioSelect,
    )
    
    class Meta:
        model = Honk
        fields = ('honked', 'clown')
    

    def __init__(self, *args, **kwargs):
        honker_id = kwargs.pop('honker_id')
        super().__init__(*args, **kwargs)
        self.fields['honked'].queryset = User.objects.exclude(id=honker_id)


