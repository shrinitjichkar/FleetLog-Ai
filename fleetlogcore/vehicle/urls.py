from django.urls import path
from .views import VehicleListCreateView, VehicleDetailView

urlpatterns = [
    path('vehicles/', VehicleListCreateView.as_view(), name='vehicle-list-create'),
    path('vehicles/<uuid:pk>/', VehicleDetailView.as_view(), name='vehicle-detail'),
]