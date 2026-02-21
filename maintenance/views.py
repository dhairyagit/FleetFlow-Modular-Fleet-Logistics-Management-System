from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MaintenanceLog, FuelLog, Expense
from .forms import MaintenanceLogForm, FuelLogForm, ExpenseForm
from vehicles.models import Vehicle

@login_required
def maintenance_list(request):
    maintenance_logs = MaintenanceLog.objects.select_related('vehicle').all()
    
    vehicle_id = request.GET.get('vehicle')
    status = request.GET.get('status')
    
    if vehicle_id:
        maintenance_logs = maintenance_logs.filter(vehicle_id=vehicle_id)
    if status:
        maintenance_logs = maintenance_logs.filter(status=status)
    
    context = {
        'maintenance_logs': maintenance_logs,
        'vehicles': Vehicle.objects.all(),
        'status_choices': MaintenanceLog.STATUS_CHOICES,
    }
    return render(request, 'maintenance/maintenance_list.html', context)

@login_required
def maintenance_create(request):
    if request.method == 'POST':
        form = MaintenanceLogForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Maintenance log added. Vehicle status updated.')
            return redirect('maintenance_list')
    else:
        form = MaintenanceLogForm()
    
    return render(request, 'maintenance/maintenance_form.html', {'form': form, 'action': 'Create'})

@login_required
def maintenance_update(request, pk):
    log = get_object_or_404(MaintenanceLog, pk=pk)
    
    if request.method == 'POST':
        form = MaintenanceLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            messages.success(request, 'Maintenance log updated')
            return redirect('maintenance_list')
    else:
        form = MaintenanceLogForm(instance=log)
    
    return render(request, 'maintenance/maintenance_form.html', {'form': form, 'action': 'Update'})

@login_required
def fuel_list(request):
    fuel_logs = FuelLog.objects.select_related('vehicle').all()
    
    vehicle_id = request.GET.get('vehicle')
    if vehicle_id:
        fuel_logs = fuel_logs.filter(vehicle_id=vehicle_id)
    
    context = {
        'fuel_logs': fuel_logs,
        'vehicles': Vehicle.objects.all(),
    }
    return render(request, 'maintenance/fuel_list.html', context)

@login_required
def fuel_create(request):
    if request.method == 'POST':
        form = FuelLogForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fuel log added successfully')
            return redirect('fuel_list')
    else:
        form = FuelLogForm()
    
    return render(request, 'maintenance/fuel_form.html', {'form': form, 'action': 'Create'})

@login_required
def expense_list(request):
    expenses = Expense.objects.select_related('vehicle').all()
    
    vehicle_id = request.GET.get('vehicle')
    expense_type = request.GET.get('type')
    
    if vehicle_id:
        expenses = expenses.filter(vehicle_id=vehicle_id)
    if expense_type:
        expenses = expenses.filter(expense_type=expense_type)
    
    context = {
        'expenses': expenses,
        'vehicles': Vehicle.objects.all(),
        'expense_types': Expense.EXPENSE_TYPES,
    }
    return render(request, 'maintenance/expense_list.html', context)

@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense added successfully')
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    
    return render(request, 'maintenance/expense_form.html', {'form': form, 'action': 'Create'})
