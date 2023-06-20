from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class CircusModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True


class Honk(CircusModel):
    honker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='honker',
    )
    clown = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='clown',
    )
    seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.honker} honked {self.clown}'

    def get_honk(self):
        if not self.seen:
            self.seen = timezone.now()
            self.save()
        return f'{self}'

