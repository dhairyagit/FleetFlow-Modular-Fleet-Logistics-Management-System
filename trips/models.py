from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from vehicles.models import Vehicle
from drivers.models import Driver

class Trip(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('DISPATCHED', 'Dispatched'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='trips')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='trips')
    cargo_weight = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    distance = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='DRAFT')
    dispatch_date = models.DateTimeField(null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Trip {self.id} - {self.source} to {self.destination}"
    
    def clean(self):
        # Validation Rule 1: Cargo weight must not exceed vehicle capacity
        if self.cargo_weight > self.vehicle.max_capacity:
            raise ValidationError(
                f'Cargo weight ({self.cargo_weight} kg) exceeds vehicle capacity ({self.vehicle.max_capacity} kg)'
            )
        
        # Validation Rule 2: Driver license must be valid
        if not self.driver.is_license_valid():
            raise ValidationError(
                f'Driver license expired on {self.driver.license_expiry}'
            )
        
        # Validation Rule 3: Driver must be on duty
        if self.status == 'DRAFT' and self.driver.status not in ['ON_DUTY', 'ON_TRIP']:
            raise ValidationError(
                f'Driver status is {self.driver.get_status_display()}. Must be On Duty.'
            )
        
        # Validation Rule 4: Vehicle must be available
        if self.status == 'DRAFT' and not self.vehicle.is_available_for_dispatch():
            raise ValidationError(
                f'Vehicle status is {self.vehicle.get_status_display()}. Must be Available.'
            )
    
    def dispatch(self):
        """Dispatch the trip and update statuses"""
        from django.utils import timezone
        
        self.status = 'DISPATCHED'
        self.dispatch_date = timezone.now()
        self.save()
        
        # Update vehicle and driver status
        self.vehicle.status = 'ON_TRIP'
        self.vehicle.save()
        
        self.driver.status = 'ON_TRIP'
        self.driver.save()
    
    def complete(self, distance_traveled):
        """Complete the trip and update statuses"""
        from django.utils import timezone
        
        self.status = 'COMPLETED'
        self.completion_date = timezone.now()
        self.distance = distance_traveled
        self.save()
        
        # Update vehicle odometer and status
        self.vehicle.odometer += distance_traveled
        self.vehicle.status = 'AVAILABLE'
        self.vehicle.save()
        
        # Update driver status
        self.driver.status = 'ON_DUTY'
        self.driver.save()
    
    def cancel(self):
        """Cancel the trip and revert statuses"""
        self.status = 'CANCELLED'
        self.save()
        
        if self.vehicle.status == 'ON_TRIP':
            self.vehicle.status = 'AVAILABLE'
            self.vehicle.save()
        
        if self.driver.status == 'ON_TRIP':
            self.driver.status = 'ON_DUTY'
            self.driver.save()
    
    class Meta:
        db_table = 'trips'
        ordering = ['-created_at']
