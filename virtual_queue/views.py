from .serializer import ServiceSerializer
from rest_framework.response import Response
from .models import User,Services,Queue,QueueParticipant
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
    if not service_id or not preferred_time:
        return Response("Please provide a service_id in the request data", status=status.HTTP_400_BAD_REQUEST)

    service = get_object_or_404(Services, id=service_id)
    user_perfferred_time =  datetime.datetime.strptime(preferred_time, "%Y-%m-%dT%H:%M:%S.%fZ")

    preferred_time_exist = get_object_or_404(Queue, service=service, preferred_time=user_perfferred_time)
    if preferred_time_exist:
        return Response(f'perferred time is already taken, please choose any other option')
    try:
        with transaction.atomic():
            # Try to get an existing open queue or create a new one if not available
            queue, created = Queue.objects.get_or_create(
                service=service,
                queue_status='open',
                defaults={
                    'max_capacity': 20,
                    'current_wait_time': timezone.now(),
                    'estimated_wait_time': 0,
                    'current_queue_size': 0,
                }
            )

            if not created and queue.current_queue_size >= queue.max_capacity:
                return Response(f'The queue for the service {service.name if service.name else ""} is currently full', status=status.HTTP_400_BAD_REQUEST)

            user_participation = QueueParticipant.objects.filter(participant=request.user, queue=queue).first()

            if user_participation:
                return Response("You've already joined the queue, wait for your turn to come", status=status.HTTP_400_BAD_REQUEST)

            # Increment current_queue_size and update estimated_wait_time atomically
            queue.current_queue_size += 1
            queue.current_wait_time += timedelta(minutes=5)
            queue.estimated_wait_time = queue.current_queue_size + 1 if queue.current_queue_size < 1 else 1
            queue.save()

            # Add your logic for joining the queue here, e.g., creating a QueueParticipant entry
            QueueParticipant.objects.create(participant=request.user, queue=queue, status='in_progress')

            return Response("Successfully joined the queue", status=status.HTTP_200_OK)

    except Exception as e:
        # Handle any exceptions that may occur during the transaction
        return Response(f"An error occurred: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)