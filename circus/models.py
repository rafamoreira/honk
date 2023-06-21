from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class CircusModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Clown(CircusModel):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='clown_images')

    def __str__(self):
        return self.name

class Honk(CircusModel):
    honker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='honks',
    )
    honked = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='honked',
    )
    clown = models.ForeignKey(
        Clown,
        on_delete=models.CASCADE,
        related_name='honks',
        null=True,
    )
    seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.honker} honked {self.honked} with {self.clown}'

    @classmethod
    def get_honks(cls, honked_id):
        honks = cls.objects.filter(
            honked_id=honked_id,
        ).order_by(
            '-created_at'
        ).select_related(
            'clown', 'honker', 'honked'
        )
        honks_list = []
        for honk in honks:
            honk_dict = {
                'honker': honk.honker.username,
                'clown_name': honk.clown.name,
                'clown_image': honk.clown.image.url,
            }
            honks_list.append(honk_dict)

        return honks_list
