from rest_framework import serializers
from .models import Inspection, ChecklistItem


class InspectionSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    vehicle_registration_no = serializers.CharField(source='vehicle.registration_no', read_only=True)

    class Meta:
        model = Inspection
        fields = [
            'id', 'tenant', 'tenant_name', 'vehicle', 'vehicle_registration_no',
            'assessor', 'supervisor', 'inspection_date', 'status', 'priority',
            'location', 'estimated_duration_minutes', 'completed_at',
            'remarks', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ChecklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistItem
        fields = ['id', 'inspection', 'label', 'category', 'is_damaged', 'severity', 'notes']
        read_only_fields = ['id']