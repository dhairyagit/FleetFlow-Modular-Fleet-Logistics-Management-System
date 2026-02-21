from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['name', 'license_plate', 'vehicle_type', 'max_capacity', 
                  'acquisition_cost', 'odometer', 'status', 'region', 'latitude', 'longitude']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'license_plate': forms.TextInput(attrs={'class': 'form-input'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-select'}),
            'max_capacity': forms.NumberInput(attrs={'class': 'form-input'}),
            'acquisition_cost': forms.NumberInput(attrs={'class': 'form-input'}),
            'odometer': forms.NumberInput(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'region': forms.TextInput(attrs={'class': 'form-input'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.000001'}),
        }
