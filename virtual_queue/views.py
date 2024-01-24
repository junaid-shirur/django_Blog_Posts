from .serializer import ServiceSerializer,QueueSerializer
from rest_framework.response import Response
from .models import User,Services,Queue, Slot
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Max
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

    try:
        service = Services.objects.get(id=service_id)
    except Services.DoesNotExist:
        return Response("Please check the service you've selected", status=status.HTTP_400_BAD_REQUEST)

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

    existing_reservation = Queue.objects.filter(
        user=request.user,
        slot=slot,
        status='in_progress' 
    ).first()

    if existing_reservation:
        return Response(f'You already have an in-progress reservation for the service {service.name} in the {preffered_slot} slot', status=status.HTTP_400_BAD_REQUEST)

    if Queue.objects.filter(date=timezone.now().date(), slot=slot, status='in_progress').count() >= slot.capacity :
        return Response(f'The {preffered_slot} slot for {service.name} is currently full', status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        max_request_number = Queue.objects.filter(slot=slot).aggregate(Max('request_number')).get('request_number') or 0

        new_request_number = max_request_number + 1
        queue = Queue.objects.create(
            user=request.user,
            status='in_progress',
            date=timezone.now().date(),
            slot=slot,
            request_number=new_request_number
        )

        serializer = QueueSerializer(queue)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

