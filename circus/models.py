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
    def get_honk(cls, honk_id) -> dict:
        """
        Get a honk by id
        """
        return cls.objects.get(id=honk_id).render_honk()

    @classmethod
    def get_sent_honks(cls, honker_id) -> list:
        """
        Get honks sent by a user and return them as a list of dicts
        """
        honks = cls.objects.filter(honker_id=honker_id).order_by('-created_at')
        return [h.render_honk() for h in honks]

    @classmethod
    def get_unread_honks(cls, honked_id) -> list:
        """
        Get honks sent to a user and return them as a list of dicts
        """
        honks = cls.objects.filter(honked_id=honked_id, seen__isnull=True)
        return [h.render_honk() for h in honks]

    @classmethod
    def get_honks(
        cls,
        honked_id=None,
        honker_id=None,
        only_unseen=False,
        mark_as_seen=False,
    ) -> list:
        """
        Get honks for a user and return them as a list of dicts
        """
        honks = cls.objects
        if honked_id:
            honks = honks.filter(honked_id=honked_id)

        if honker_id:
            honks = honks.filter(honker_id=honker_id)

        if only_unseen:
            honks = honks.filter(seen__isnull=True)

        honks.order_by('-created_at').select_related(
            'clown', 'honker', 'honked'
        )

        honks_list = [h.render_honk() for h in honks]

        if mark_as_seen:
            honks.update(seen=timezone.now())

        return honks_list

    def render_honk(self) -> dict:
        """
        Render a honk as a dict with all details to be shown on a view
        """
        return {
            'id': self.id,
            'honker': self.honker.username,
            'honked': self.honked.username,
            'clown_name': self.clown.name,
            'clown_image': self.clown.image.url,
            'clown_image_name': self.clown.image.name,
        }

    def mark_as_seen(self):
        """
        Mark a honk as seen
        """
        self.seen = timezone.now()
        self.save()
