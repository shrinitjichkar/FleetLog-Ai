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
        
        
    def validate(self, data):
        vehicle = data.get('vehicle', getattr(self.instance, 'vehicle', None))
        inspection_date = data.get('inspection_date', getattr(self.instance, 'inspection_date', None))

        if vehicle and inspection_date:
            vehicle_created_date = vehicle.created_at.date()
            if inspection_date < vehicle_created_date:
                raise serializers.ValidationError({
                    'inspection_date': f"inspection_date cannot be before the vehicle's created_at date ({vehicle_created_date})."
                })

        return data    
        
        
        


class ChecklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistItem
        fields = ['id', 'inspection', 'label', 'category', 'is_damaged', 'severity', 'notes']
        read_only_fields = ['id']