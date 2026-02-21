from django.contrib import admin
from .models import MaintenanceLog, FuelLog, Expense

@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'service_type', 'cost', 'date', 'status']
    list_filter = ['service_type', 'status', 'date']
    search_fields = ['vehicle__name', 'notes']

@admin.register(FuelLog)
class FuelLogAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'liters', 'fuel_cost', 'date', 'odometer_reading']
    list_filter = ['date']
    search_fields = ['vehicle__name']

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'expense_type', 'amount', 'date']
    list_filter = ['expense_type', 'date']
    search_fields = ['vehicle__name', 'description']
