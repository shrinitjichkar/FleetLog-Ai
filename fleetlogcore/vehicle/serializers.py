from rest_framework import serializers
from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)

    class Meta:
        model = Vehicle
        fields = [
            'id', 'tenant', 'tenant_name', 'registration_no',
            'make', 'model', 'year', 'vehicle_type', 'body_type', 'color',
            'fuel_type', 'transmission_type', 'seating_capacity', 'engine_capacity_cc',
            'odometer', 'insurance_expiry_date', 'last_service_date',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_odometer(self, value):
         if self.instance is not None and value < self.instance.odometer:
             raise serializers.ValidationError(
                 f"odometer cannot decrease. Current value is {self.instance.odometer}."
             )
         return value