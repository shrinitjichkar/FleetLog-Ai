import uuid
from django.db import models
from accounts.models import Tenant, User
from vehicle.models import Vehicle


class Inspection(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_review', 'In Review'),
        ('completed', 'Completed'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='inspections')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='inspections')
    assessor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_inspections')
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='supervised_inspections')

    inspection_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')

    location = models.CharField(max_length=255, default='Unknown')
    estimated_duration_minutes = models.PositiveIntegerField(default=60)
    completed_at = models.DateTimeField(null=True, blank=True)

    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vehicle.registration_no} - {self.status}"


class ChecklistItem(models.Model):
    SEVERITY_CHOICES = [
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
    ]
    CATEGORY_CHOICES = [
        ('exterior', 'Exterior'),
        ('interior', 'Interior'),
        ('mechanical', 'Mechanical'),
        ('electrical', 'Electrical'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='checklist_items')
    label = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True)
    is_damaged = models.BooleanField(default=False)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.label} ({'damaged' if self.is_damaged else 'ok'})"