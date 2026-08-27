from rest_framework import serializers
from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'tenant', 'registration_no', 'odometer', 'created_at']
        read_only_fields = ['id', 'created_at']