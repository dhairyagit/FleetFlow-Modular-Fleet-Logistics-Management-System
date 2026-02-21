from django.db import models
from django.core.validators import MinValueValidator

class Vehicle(models.Model):
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('ON_TRIP', 'On Trip'),
        ('IN_SHOP', 'In Shop'),
        ('SUSPENDED', 'Suspended'),
        ('RETIRED', 'Retired'),
    ]
    
    TYPE_CHOICES = [
        ('TRUCK', 'Truck'),
        ('VAN', 'Van'),
        ('BIKE', 'Bike'),
    ]
    
    name = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    max_capacity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    acquisition_cost = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    odometer = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='AVAILABLE')
    region = models.CharField(max_length=50, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    last_location_update = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.license_plate})"
    
    def is_available_for_dispatch(self):
        return self.status == 'AVAILABLE'
    
    def total_maintenance_cost(self):
        return self.maintenance_logs.aggregate(models.Sum('cost'))['cost__sum'] or 0
    
    def total_fuel_cost(self):
        return self.fuel_logs.aggregate(models.Sum('fuel_cost'))['fuel_cost__sum'] or 0
    
    def total_revenue(self):
        return self.trips.filter(status='COMPLETED').aggregate(models.Sum('revenue'))['revenue__sum'] or 0
    
    def roi(self):
        revenue = self.total_revenue()
        costs = self.total_maintenance_cost() + self.total_fuel_cost()
        if self.acquisition_cost > 0:
            return ((revenue - costs) / self.acquisition_cost) * 100
        return 0
    
    class Meta:
        db_table = 'vehicles'
        ordering = ['-created_at']
