from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Trip
from .forms import TripForm, TripCompleteForm
from vehicles.models import Vehicle
from drivers.models import Driver

@login_required
def trip_list(request):
    trips = Trip.objects.select_related('vehicle', 'driver').all()
    
    # Filters
    status_filter = request.GET.get('status')
    vehicle_id = request.GET.get('vehicle')
    driver_id = request.GET.get('driver')
    
    if status_filter:
        trips = trips.filter(status=status_filter)
    if vehicle_id:
        trips = trips.filter(vehicle_id=vehicle_id)
    if driver_id:
        trips = trips.filter(driver_id=driver_id)
    
    context = {
        'trips': trips,
        'status_choices': Trip.STATUS_CHOICES,
        'vehicles': Vehicle.objects.all(),
        'drivers': Driver.objects.all(),
    }
    return render(request, 'trips/trip_list.html', context)

@login_required
def trip_create(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            try:
                trip = form.save(commit=False)
                trip.full_clean()  # Run validation
                trip.save()
                messages.success(request, 'Trip created successfully')
                return redirect('trip_list')
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)
    else:
        form = TripForm()
    
    # Get available vehicles and drivers
    available_vehicles = Vehicle.objects.filter(status='AVAILABLE')
    available_drivers = Driver.objects.filter(status='ON_DUTY')
    
    context = {
        'form': form,
        'action': 'Create',
        'available_vehicles': available_vehicles,
        'available_drivers': available_drivers,
    }
    return render(request, 'trips/trip_form.html', context)

@login_required
def trip_update(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    
    if trip.status != 'DRAFT':
        messages.error(request, 'Only draft trips can be edited')
        return redirect('trip_list')
    
    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            try:
                trip = form.save(commit=False)
                trip.full_clean()
                trip.save()
                messages.success(request, 'Trip updated successfully')
                return redirect('trip_list')
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)
    else:
        form = TripForm(instance=trip)
    
    context = {
        'form': form,
        'action': 'Update',
        'trip': trip,
    }
    return render(request, 'trips/trip_form.html', context)

@login_required
def trip_dispatch(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    
    if trip.status != 'DRAFT':
        messages.error(request, 'Only draft trips can be dispatched')
        return redirect('trip_list')
    
    try:
        trip.full_clean()
        trip.dispatch()
        messages.success(request, f'Trip dispatched successfully. Vehicle and driver are now On Trip.')
        return redirect('trip_list')
    except ValidationError as e:
        for error in e.messages:
            messages.error(request, error)
        return redirect('trip_list')

@login_required
def trip_complete(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    
    if trip.status != 'DISPATCHED':
        messages.error(request, 'Only dispatched trips can be completed')
        return redirect('trip_list')
    
    if request.method == 'POST':
        form = TripCompleteForm(request.POST)
        if form.is_valid():
            distance = form.cleaned_data['distance_traveled']
            trip.complete(distance)
            messages.success(request, f'Trip completed. Odometer updated by {distance} km.')
            return redirect('trip_list')
    else:
        form = TripCompleteForm()
    
    return render(request, 'trips/trip_complete.html', {'trip': trip, 'form': form})

@login_required
def trip_cancel(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    
    if trip.status == 'COMPLETED':
        messages.error(request, 'Completed trips cannot be cancelled')
        return redirect('trip_list')
    
    if request.method == 'POST':
        trip.cancel()
        messages.success(request, 'Trip cancelled. Vehicle and driver statuses reverted.')
        return redirect('trip_list')
    
    return render(request, 'trips/trip_confirm_cancel.html', {'trip': trip})

@login_required
def trip_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    return render(request, 'trips/trip_detail.html', {'trip': trip})
