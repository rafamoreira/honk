from django.contrib.auth.models import User

from circus.models import Honk
from rest_framework import serializers


class HonkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Honk
        fields = ['url', 'id', 'created_at', 'updated_at']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username']
