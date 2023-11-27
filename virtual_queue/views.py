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

    if not service_id:
        return Response("Please provide a service_id in the request data", status=status.HTTP_400_BAD_REQUEST)

    service = get_object_or_404(Services, id=service_id)

    try:
        with transaction.atomic():
            # Try to get an existing open queue or create a new one if not available
            queue = Queue.objects.filter(
                service=service,
                queue_status='open',
                current_queue_size__lt=F('max_capacity')
            ).select_for_update().first()

            if not queue:
                # If the queue doesn't exist, create a new one
                queue = Queue.objects.create(
                    service=service,
                    queue_status='open',
                    max_capacity=20,
                )

            if queue.current_queue_size >= queue.max_capacity:
                return Response(f'The queue for the service {service.name if service.name else ""} is currently full', status=status.HTTP_400_BAD_REQUEST)

            user_participation = QueueParticipant.objects.filter(participant=request.user, queue=queue).first()

            if user_participation:
                return Response("You've already join the queue, wait your turn to come", status=status.HTTP_400_BAD_REQUEST)

            # Add your logic for joining the queue here, e.g., creating a QueueParticipant entry
            QueueParticipant.objects.create(participant=request.user, queue=queue, status='pending')
            # Increment current_queue_size atomically
            queue.current_queue_size += 1
            queue.current_wait_time += timedelta(minutes=5)
            queue.estimated_wait_time = queue.current_queue_size - 1
            queue.save()
            return Response("Successfully joined the queue", status=status.HTTP_200_OK)

    except Exception as e:
        # Handle any exceptions that may occur during the transaction
        return Response(f"An error occurred: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


