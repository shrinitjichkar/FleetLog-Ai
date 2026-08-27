from django.contrib import admin

# Register your models here.

from .models import Inspection,ChecklistItem

admin.site.register(Inspection)
admin.site.register(ChecklistItem)