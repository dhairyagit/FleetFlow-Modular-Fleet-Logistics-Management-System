from django.contrib import admin
from .models import Vehicle

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['name', 'license_plate', 'vehicle_type', 'status', 'max_capacity', 'odometer']
    list_filter = ['status', 'vehicle_type', 'region']
    search_fields = ['name', 'license_plate']
