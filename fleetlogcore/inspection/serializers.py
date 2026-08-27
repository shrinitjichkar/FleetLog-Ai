from rest_framework import serializers
from .models import Inspection, ChecklistItem


class InspectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inspection
        fields = ['id', 'tenant', 'vehicle', 'assessor', 'inspection_date', 'status']
        read_only_fields = ['id']


class ChecklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistItem
        fields = ['id', 'inspection', 'label', 'is_damaged', 'notes']
        read_only_fields = ['id']