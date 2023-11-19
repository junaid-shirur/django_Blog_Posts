from .serializer import ServiceSerializer
from rest_framework.response import Response
from .models import User,Services,Queue,QueueParticipant
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
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

    service = get_object_or_404(Services, id=request.service_id)
    queue = Queue.objects.filter(service=service, queue_status='open', current_queue_size__lt=20).first()
    if not queue :
       return Response(f'currently queue is not available for the service {service if service.name else ""}', status=status.HTTP_400_BAD_REQUEST)
    
    user_participation = QueueParticipant.objects.filter(participant=request.user, queue=queue).first()

    if user_participation :
        return Response("user already in queue, wait your turn comes", status=status.HTTP_400_BAD_REQUEST)