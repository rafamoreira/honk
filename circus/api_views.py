"""
api_views.py

This file contains the API views for the circus app.
"""
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from circus.models import Honk
from circus.serializers import HonkSerializer


class ListHonks(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HonkSerializer

    @staticmethod
    def get(request):
        """
        /api/honks
        """
        honks = Honk.objects.filter(honked=request.user)
        serializer = HonkSerializer(honks, many=True)
        return Response(serializer.data)


class ListUnreadHonks(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HonkSerializer

    @staticmethod
    def get(request):
        """
        /api/unread_honks
        """
        honks = Honk.objects.filter(honked=request.user, seen__isnull=True)
        serializer = HonkSerializer(honks, many=True)
        return Response(serializer.data)


class ReadHonk(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HonkSerializer

    @staticmethod
    def get(request, pk):
        """
        /api/read_honk
        """
        honk = Honk.objects.get(pk=pk)
        if honk.honked != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        honk.mark_as_seen()
        honk.refresh_from_db()
        serializer = HonkSerializer(honk)
        return Response(serializer.data)
