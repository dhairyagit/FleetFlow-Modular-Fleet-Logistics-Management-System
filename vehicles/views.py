from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Vehicle
from .forms import VehicleForm

@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    
    # Filters
    status_filter = request.GET.get('status')
    vehicle_type = request.GET.get('type')
    region = request.GET.get('region')
    search = request.GET.get('search')
    
    if status_filter:
        vehicles = vehicles.filter(status=status_filter)
    if vehicle_type:
        vehicles = vehicles.filter(vehicle_type=vehicle_type)
    if region:
        vehicles = vehicles.filter(region__icontains=region)
    if search:
        vehicles = vehicles.filter(
            Q(name__icontains=search) | Q(license_plate__icontains=search)
        )
    
    context = {
        'vehicles': vehicles,
        'status_choices': Vehicle.STATUS_CHOICES,
        'type_choices': Vehicle.TYPE_CHOICES,
    }
    return render(request, 'vehicles/vehicle_list.html', context)

@login_required
def vehicle_create(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle added successfully')
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    
    return render(request, 'vehicles/vehicle_form.html', {'form': form, 'action': 'Create'})

@login_required
def vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle updated successfully')
            return redirect('vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    
    return render(request, 'vehicles/vehicle_form.html', {'form': form, 'action': 'Update'})

@login_required
def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'Vehicle deleted successfully')
        return redirect('vehicle_list')
    
    return render(request, 'vehicles/vehicle_confirm_delete.html', {'vehicle': vehicle})

@login_required
def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    
    context = {
        'vehicle': vehicle,
        'maintenance_logs': vehicle.maintenance_logs.all()[:10],
        'fuel_logs': vehicle.fuel_logs.all()[:10],
        'trips': vehicle.trips.all()[:10],
    }
    
    return render(request, 'vehicles/vehicle_detail.html', context)
