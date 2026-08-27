from django.db import models
import uuid
from accounts.models import Tenant


class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='vehicles'
    )
    registration_no = models.CharField(max_length=20, unique=True)
    odometer = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.registration_no