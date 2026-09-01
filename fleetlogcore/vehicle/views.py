from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404


from .models import Vehicle
from .serializers import VehicleSerializer

from accounts.permissions import IsRenter, IsRenterOrSupervisor
from rest_framework.permissions import IsAuthenticated

from rest_framework.pagination import PageNumberPagination

from .filters import VehicleFilter





class VehicleListCreateView(APIView):
    pagination_class = PageNumberPagination
    
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsRenter()]
        return [IsAuthenticated()]
    
    
    def get(self, request):
        vehicles = Vehicle.objects.all()
        
        vehicle_filter = VehicleFilter(request.query_params, queryset=vehicles)
        vehicles = vehicle_filter.qs
        
        
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(vehicles, request)   
        serializer = VehicleSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    
    def post(self, request):
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VehicleDetailView(APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsRenterOrSupervisor()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data)

    def put(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        serializer = VehicleSerializer(vehicle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        serializer = VehicleSerializer(vehicle, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        vehicle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)