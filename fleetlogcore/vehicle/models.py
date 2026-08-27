import uuid
from django.db import models
from django.core.validators import RegexValidator
from accounts.models import Tenant


registration_no_validator = RegexValidator(
    regex=r'^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$',
    message="registration_no must match format: MH12AB1234"
)


class Vehicle(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('car', 'Car'),
        ('bike', 'Bike'),
        ('truck', 'Truck'),
        ('van', 'Van'),
    ]
    BODY_TYPE_CHOICES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('hatchback', 'Hatchback'),
        ('coupe', 'Coupe'),
        ('convertible', 'Convertible'),
        ('pickup', 'Pickup'),
        ('minivan', 'Minivan'),
        ('not_applicable', 'Not Applicable'),
    ]
    FUEL_TYPE_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
        ('cng', 'CNG'),
    ]
    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='vehicles')

    registration_no = models.CharField(max_length=20, unique=True, validators=[registration_no_validator])

    make = models.CharField(max_length=100, default='Unknown')
    model = models.CharField(max_length=100, default='Unknown')
    year = models.PositiveIntegerField(default=2020)

    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICES, default='car')
    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES, default='sedan')
    color = models.CharField(max_length=50, default='Unknown')
    fuel_type = models.CharField(max_length=10, choices=FUEL_TYPE_CHOICES, default='petrol')
    transmission_type = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES, default='manual')

    seating_capacity = models.PositiveIntegerField(default=5)
    engine_capacity_cc = models.PositiveIntegerField(default=1200)

    odometer = models.IntegerField()
    insurance_expiry_date = models.DateField(null=True, blank=True)
    last_service_date = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.registration_no} ({self.make} {self.model})"