"""
api_views.py

This file contains the API views for the circus app.
"""
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from circus.models import Honk
from circus.serializers import HonkSerializer, UserSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def honk_list(request):
    """
    /honk_list
    """
    if request.method == 'GET':
        honks = Honk.objects.all()
        serializer = HonkSerializer(honks, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = HonkSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def honk_detail(request, pk):
    """
    /honk_detail
    """
    try:
        honk = Honk.objects.get(pk=pk)
    except Honk.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = HonkSerializer(honk)
        return JsonResponse(serializer.data)

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = HonkSerializer(honk, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    if request.method == 'DELETE':
        honk.delete()
        return HttpResponse(status=204)


class UserList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
# API_VIEWS END
