from django.contrib import admin
from .models import Trip

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['id', 'vehicle', 'driver', 'source', 'destination', 'status', 'created_at']
    list_filter = ['status', 'dispatch_date', 'completion_date']
    search_fields = ['source', 'destination', 'vehicle__name', 'driver__name']
