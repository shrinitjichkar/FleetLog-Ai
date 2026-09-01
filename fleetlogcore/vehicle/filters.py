from django_filters import rest_framework as filters
from .models import Vehicle

class VehicleFilter(filters.FilterSet):
    class Meta:
        model = Vehicle
        fields = ['vehicle_type', 'body_type', 'fuel_type', 'is_active']