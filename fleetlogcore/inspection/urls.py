from django.urls import path
from .views import (
    InspectionListCreateView, InspectionDetailView,
    ChecklistItemListCreateView, ChecklistItemDetailView,
)

urlpatterns = [
    path('inspections/', InspectionListCreateView.as_view(), name='inspection-list-create'),
    path('inspections/<uuid:pk>/', InspectionDetailView.as_view(), name='inspection-detail'),
    path('checklist-items/', ChecklistItemListCreateView.as_view(), name='checklist-list-create'),
    path('checklist-items/<uuid:pk>/', ChecklistItemDetailView.as_view(), name='checklist-detail'),
]