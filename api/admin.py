"""Customize admin interface."""

from django.contrib import admin
from api.models import Flight

# Register your models here.
@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    """Flight admin customization."""
    pass
