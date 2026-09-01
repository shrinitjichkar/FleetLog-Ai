from django_filters import rest_framework as filters
from .models import Inspection


class InspectionFilter(filters.FilterSet):
    class Meta:
        model = Inspection
        fields = ['status', 'priority']