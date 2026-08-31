from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class Tenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLE_CHOICES = [
        ('renter', 'Renter'),
        ('supervisor', 'Supervisor'),
        ('assessor', 'Assessor'),
    ]


    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='users',
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
    
    