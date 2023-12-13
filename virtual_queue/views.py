from .serializer import ServiceSerializer,QueueSerializer
from rest_framework.response import Response
from .models import User,Services,Queue, Slot
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import date, timedelta
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


from django.db import transaction
from django.db.models import F
from django.utils import timezone

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def joinQueue(request):
    service_id = request.data.get('service_id')
    preffered_slot = request.data.get('preffered_slot')

    if not service_id or not preffered_slot:
        return Response("Please provide both service_id and preffered_slot in the request data", status=status.HTTP_400_BAD_REQUEST)

    service = Services.objects.get(id=service_id)

    # Assuming preffered_slot is a string representing a slot, e.g., 'morning'
    try:
        slot = Slot.objects.get(service=service, slot=preffered_slot)
    except Slot.DoesNotExist:
        slot = Slot.objects.create(
            service=service,
            slot=preffered_slot,
            start_time=timezone.now().time(),  # You may adjust this based on your requirements
            end_time=(timezone.now() + datetime.timedelta(hours=3)).time(),  # Adjust the end time accordingly
            capacity=5,  # Set the initial capacity for the new slot
        )

    # Check if someone has already reserved the queue for the same service, date, and slot
    existing_reservation = Queue.objects.filter(
        user=request.user,
        slot=slot,
        status='in_progress' 
    ).first()

    if existing_reservation:
        return Response(f'You already have an in-progress reservation for the service {service.name} in the {preffered_slot} slot', status=status.HTTP_400_BAD_REQUEST)

    # Check if the preferred slot is available
    if Queue.objects.filter(date=timezone.now().date(), slot=slot, status='in_progress').count() >= slot.capacity :
        return Response(f'The {preffered_slot} slot for {service.name} is currently full', status=status.HTTP_400_BAD_REQUEST)

    # Generate a unique queue token (you may use a more sophisticated method)

    # Create a queue reservation
    with transaction.atomic():
        queue = Queue.objects.create(
            user=request.user,
            status='in_progress',
            date=timezone.now().date(),
            slot=slot,
            request_number=Queue.objects.get(slot=slot).request_number + 1
        )

        serializer = QueueSerializer(queue)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

