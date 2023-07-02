from django.contrib.auth.models import User

from circus.models import Honk
from rest_framework import serializers


class HonkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Honk
        fields = ['id', 'honker', 'clown', 'clown_url', 'created_at']

    honker = serializers.ReadOnlyField(source='honker.username')
    clown = serializers.ReadOnlyField(source='clown.name')
    clown_url = serializers.ReadOnlyField(source='clown.image.url')
