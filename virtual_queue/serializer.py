from rest_framework import serializers
from .models import Services,Slot, Queue
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ['id', 'start_time', 'end_time', 'capacity']

class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = ['id', 'slot', 'date', 'user','request_number']

