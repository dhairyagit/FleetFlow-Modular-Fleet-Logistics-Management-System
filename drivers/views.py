from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Driver
from .forms import DriverForm

@login_required
def driver_list(request):
    drivers = Driver.objects.all()
    
    # Filters
    status_filter = request.GET.get('status')
    search = request.GET.get('search')
    
    if status_filter:
        drivers = drivers.filter(status=status_filter)
    if search:
        drivers = drivers.filter(
            Q(name__icontains=search) | Q(license_number__icontains=search)
        )
    
    context = {
        'drivers': drivers,
        'status_choices': Driver.STATUS_CHOICES,
    }
    return render(request, 'drivers/driver_list.html', context)

@login_required
def driver_create(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Driver added successfully')
            return redirect('driver_list')
    else:
        form = DriverForm()
    
    return render(request, 'drivers/driver_form.html', {'form': form, 'action': 'Create'})

@login_required
def driver_update(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    
    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            messages.success(request, 'Driver updated successfully')
            return redirect('driver_list')
    else:
        form = DriverForm(instance=driver)
    
    return render(request, 'drivers/driver_form.html', {'form': form, 'action': 'Update'})

@login_required
def driver_delete(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    
    if request.method == 'POST':
        driver.delete()
        messages.success(request, 'Driver deleted successfully')
        return redirect('driver_list')
    
    return render(request, 'drivers/driver_confirm_delete.html', {'driver': driver})

@login_required
def driver_detail(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    
    context = {
        'driver': driver,
        'trips': driver.trips.all()[:10],
        'total_trips': driver.total_trips(),
        'completed_trips': driver.completed_trips(),
        'completion_rate': round(driver.completion_rate(), 1),
        'safety_score': round(driver.safety_score(), 1),
    }
    
    return render(request, 'drivers/driver_detail.html', context)
