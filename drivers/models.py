from django.db import models
from django.utils import timezone
from vehicles.models import Vehicle

class Driver(models.Model):
    STATUS_CHOICES = [
        ('ON_DUTY', 'On Duty'),
        ('OFF_DUTY', 'Off Duty'),
        ('ON_TRIP', 'On Trip'),
        ('SUSPENDED', 'Suspended'),
    ]
    
    LICENSE_CHOICES = [
        ('A', 'Category A - Motorcycle'),
        ('B', 'Category B - Car/Van'),
        ('C', 'Category C - Truck'),
        ('D', 'Category D - Bus'),
    ]
    
    name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    license_category = models.CharField(max_length=5, choices=LICENSE_CHOICES)
    license_expiry = models.DateField()
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='OFF_DUTY')
    assigned_vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_drivers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.license_number})"
    
    def is_license_valid(self):
        return self.license_expiry >= timezone.now().date()
    
    def is_available_for_dispatch(self):
        return self.status == 'ON_DUTY' and self.is_license_valid()
    
    def total_trips(self):
        return self.trips.count()
    
    def completed_trips(self):
        return self.trips.filter(status='COMPLETED').count()
    
    def completion_rate(self):
        total = self.total_trips()
        if total > 0:
            return (self.completed_trips() / total) * 100
        return 0
    
    def safety_score(self):
        # Simple safety score based on completion rate
        return min(100, self.completion_rate())
    
    class Meta:
        db_table = 'drivers'
        ordering = ['-created_at']
