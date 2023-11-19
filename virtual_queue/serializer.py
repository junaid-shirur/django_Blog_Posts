from rest_framework import serializers
from .models import Services, QueueParticipant
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'


class QueueParticipantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueueParticipant