from django import forms
from .models import Driver

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'license_number', 'license_category', 'license_expiry', 
                  'phone', 'status', 'assigned_vehicle']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'license_number': forms.TextInput(attrs={'class': 'form-input'}),
            'license_category': forms.Select(attrs={'class': 'form-select'}),
            'license_expiry': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'assigned_vehicle': forms.Select(attrs={'class': 'form-select'}),
        }
