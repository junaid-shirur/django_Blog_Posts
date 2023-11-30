from .serializer import ServiceSerializer
from rest_framework.response import Response
from .models import User,Services,Queue
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from django.db.models import F
import datetime
# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getServices(request):
    user = request.user
    if not user :
       return Response("Please login", status=status.HTTP_400_BAD_REQUEST)
    services = Services.objects.all()
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createService(request):
    user = request.user
    if not user:
        return Response("Please login", status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def joinQueue(request):
    service_id = request.data.get('service_id')
    preferred_time = request.data.get('preferred_time')
