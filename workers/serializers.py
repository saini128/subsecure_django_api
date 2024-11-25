from rest_framework import serializers
from .models import Worker, Location, EventLog

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        extra_kwargs = {
            'humidity': {'required': False},
            'temperature': {'required': False}
        }

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'
        #location is not needed
        extra_kwargs = {
            'location': {'required': False}
        }
class EventLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLog
        fields = '__all__'
        extra_kwargs = {
            'worker': {'required': False}
        }