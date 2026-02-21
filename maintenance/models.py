from django.db import models
from django.core.validators import MinValueValidator
from vehicles.models import Vehicle

class MaintenanceLog(models.Model):
    SERVICE_TYPES = [
        ('OIL_CHANGE', 'Oil Change'),
        ('TIRE_REPLACEMENT', 'Tire Replacement'),
        ('BRAKE_SERVICE', 'Brake Service'),
        ('ENGINE_REPAIR', 'Engine Repair'),
        ('BODY_WORK', 'Body Work'),
        ('INSPECTION', 'Inspection'),
        ('OTHER', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_logs')
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.vehicle.name} - {self.get_service_type_display()} - {self.date}"
    
    def save(self, *args, **kwargs):
        # Auto-update vehicle status based on maintenance status
        if self.status in ['PENDING', 'IN_PROGRESS']:
            self.vehicle.status = 'IN_SHOP'
            self.vehicle.save()
        elif self.status == 'COMPLETED':
            # Only set to available if no other pending maintenance
            other_pending = MaintenanceLog.objects.filter(
                vehicle=self.vehicle,
                status__in=['PENDING', 'IN_PROGRESS']
            ).exclude(pk=self.pk).exists()
            
            if not other_pending:
                self.vehicle.status = 'AVAILABLE'
                self.vehicle.save()
        
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'maintenance_logs'
        ordering = ['-date']


class FuelLog(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='fuel_logs')
    liters = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    fuel_cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    date = models.DateField()
    odometer_reading = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.vehicle.name} - {self.liters}L - {self.date}"
    
    def cost_per_liter(self):
        if self.liters > 0:
            return self.fuel_cost / self.liters
        return 0
    
    class Meta:
        db_table = 'fuel_logs'
        ordering = ['-date']


class Expense(models.Model):
    EXPENSE_TYPES = [
        ('FUEL', 'Fuel'),
        ('MAINTENANCE', 'Maintenance'),
        ('INSURANCE', 'Insurance'),
        ('REGISTRATION', 'Registration'),
        ('PARKING', 'Parking'),
        ('TOLLS', 'Tolls'),
        ('OTHER', 'Other'),
    ]
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='expenses')
    expense_type = models.CharField(max_length=20, choices=EXPENSE_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.vehicle.name} - {self.get_expense_type_display()} - ₹{self.amount}"
    
    class Meta:
        db_table = 'expenses'
        ordering = ['-date']
