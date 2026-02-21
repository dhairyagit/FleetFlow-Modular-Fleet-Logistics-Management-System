from django import forms
from .models import MaintenanceLog, FuelLog, Expense

class MaintenanceLogForm(forms.ModelForm):
    class Meta:
        model = MaintenanceLog
        fields = ['vehicle', 'service_type', 'cost', 'date', 'status', 'notes']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-select'}),
            'service_type': forms.Select(attrs={'class': 'form-select'}),
            'cost': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }

class FuelLogForm(forms.ModelForm):
    class Meta:
        model = FuelLog
        fields = ['vehicle', 'liters', 'fuel_cost', 'date', 'odometer_reading', 'notes']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-select'}),
            'liters': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'fuel_cost': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'odometer_reading': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['vehicle', 'expense_type', 'amount', 'date', 'description']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-select'}),
            'expense_type': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }
