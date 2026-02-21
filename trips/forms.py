from django import forms
from .models import Trip

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['vehicle', 'driver', 'cargo_weight', 'source', 'destination', 'revenue', 'notes']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-select'}),
            'driver': forms.Select(attrs={'class': 'form-select'}),
            'cargo_weight': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'source': forms.TextInput(attrs={'class': 'form-input'}),
            'destination': forms.TextInput(attrs={'class': 'form-input'}),
            'revenue': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }

class TripCompleteForm(forms.Form):
    distance_traveled = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'})
    )
