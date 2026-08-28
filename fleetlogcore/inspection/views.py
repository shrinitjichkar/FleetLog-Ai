from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Inspection, ChecklistItem
from .serializers import InspectionSerializer, ChecklistItemSerializer

from accounts.permissions import IsRenterOrSupervisor, IsSupervisorOrAssessor





class InspectionListCreateView(APIView):
    

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsRenterOrSupervisor()]
        return []
    
    
    def get(self, request):
        inspections = Inspection.objects.all()
        serializer = InspectionSerializer(inspections, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InspectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InspectionDetailView(APIView):
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsSupervisorOrAssessor()]
        return []

    
    
    def get(self, request, pk):
        inspection = get_object_or_404(Inspection, pk=pk)
        serializer = InspectionSerializer(inspection)
        return Response(serializer.data)

    def put(self, request, pk):
        inspection = get_object_or_404(Inspection, pk=pk)
        serializer = InspectionSerializer(inspection, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        inspection = get_object_or_404(Inspection, pk=pk)
        serializer = InspectionSerializer(inspection, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        inspection = get_object_or_404(Inspection, pk=pk)
        inspection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChecklistItemListCreateView(APIView):
    def get(self, request):
        items = ChecklistItem.objects.all()
        serializer = ChecklistItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChecklistItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChecklistItemDetailView(APIView):
    def get(self, request, pk):
        item = get_object_or_404(ChecklistItem, pk=pk)
        serializer = ChecklistItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        item = get_object_or_404(ChecklistItem, pk=pk)
        serializer = ChecklistItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = get_object_or_404(ChecklistItem, pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)