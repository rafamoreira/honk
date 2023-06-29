from django.contrib.auth.models import User

from circus.models import Honk
from rest_framework import serializers


class HonkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Honk
        fields = ['id', 'created_at', 'updated_at', 'honker']

    honker = serializers.ReadOnlyField(source='honker.username')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
