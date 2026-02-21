from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum, Count, Avg, F, Q
from django.utils import timezone
from datetime import timedelta
import csv
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from vehicles.models import Vehicle
from drivers.models import Driver
from trips.models import Trip
from maintenance.models import MaintenanceLog, FuelLog

@login_required
def analytics_dashboard(request):
    # Date range filter
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)
    
    # Fleet Utilization
    total_vehicles = Vehicle.objects.exclude(status='RETIRED').count()
    active_vehicles = Vehicle.objects.filter(status='ON_TRIP').count()
    fleet_utilization = (active_vehicles / total_vehicles * 100) if total_vehicles > 0 else 0
    
    # Fuel Efficiency
    fuel_data = FuelLog.objects.filter(date__gte=start_date).aggregate(
        total_liters=Sum('liters'),
        total_cost=Sum('fuel_cost')
    )
    
    trip_data = Trip.objects.filter(
        status='COMPLETED',
        completion_date__gte=start_date
    ).aggregate(
        total_distance=Sum('distance')
    )
    
    total_distance = float(trip_data['total_distance'] or 0)
    total_liters = float(fuel_data['total_liters'] or 0)
    fuel_efficiency = (total_distance / total_liters) if total_liters > 0 else 0
    
    # Cost per KM
    maintenance_cost = MaintenanceLog.objects.filter(
        date__gte=start_date,
        status='COMPLETED'
    ).aggregate(total=Sum('cost'))['total'] or 0
    
    fuel_cost = fuel_data['total_cost'] or 0
    total_cost = float(maintenance_cost) + float(fuel_cost)
    cost_per_km = (total_cost / total_distance) if total_distance > 0 else 0
    
    # Vehicle ROI for charts (JSON) and tables
    vehicles_with_roi_json = []
    vehicles_with_roi_table = []
    
    try:
        for vehicle in Vehicle.objects.exclude(status='RETIRED')[:10]:
            try:
                roi_value = vehicle.roi()
                revenue_value = vehicle.total_revenue()
                costs_value = vehicle.total_maintenance_cost() + vehicle.total_fuel_cost()
                
                # For JSON (charts) - convert all to float
                vehicles_with_roi_json.append({
                    'vehicle': {'name': str(vehicle.name)},
                    'roi': float(round(roi_value, 2)),
                    'revenue': float(revenue_value),
                    'costs': float(costs_value),
                })
                
                # For table display
                vehicles_with_roi_table.append({
                    'vehicle': vehicle,
                    'roi': round(roi_value, 2),
                    'revenue': revenue_value,
                    'costs': costs_value,
                })
            except Exception as e:
                print(f"Error processing vehicle {vehicle.name}: {e}")
                continue
        
        vehicles_with_roi_json.sort(key=lambda x: x['roi'], reverse=True)
        vehicles_with_roi_table.sort(key=lambda x: x['roi'], reverse=True)
    except Exception as e:
        print(f"Error processing vehicles: {e}")
    
    # Driver Performance
    drivers_performance = []
    try:
        for driver in Driver.objects.all()[:10]:
            try:
                drivers_performance.append({
                    'driver': driver,
                    'total_trips': driver.total_trips(),
                    'completion_rate': round(driver.completion_rate(), 1),
                    'safety_score': round(driver.safety_score(), 1),
                })
            except Exception as e:
                print(f"Error processing driver {driver.name}: {e}")
                continue
        
        drivers_performance.sort(key=lambda x: x['safety_score'], reverse=True)
    except Exception as e:
        print(f"Error processing drivers: {e}")
    
    import json
    context = {
        'fleet_utilization': round(fleet_utilization, 1),
        'fuel_efficiency': round(fuel_efficiency, 2),
        'cost_per_km': round(cost_per_km, 2),
        'total_cost': round(total_cost, 2),
        'total_distance': round(total_distance, 2),
        'vehicles_with_roi': json.dumps(vehicles_with_roi_json[:5]),
        'vehicles_with_roi_table': vehicles_with_roi_table[:10],
        'drivers_performance': drivers_performance[:10],
        'days': days,
    }
    
    return render(request, 'analytics/dashboard.html', context)

@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fleet_analytics.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Vehicle', 'Type', 'Status', 'Total Revenue', 'Total Costs', 'ROI %'])
    
    for vehicle in Vehicle.objects.all():
        writer.writerow([
            vehicle.name,
            vehicle.get_vehicle_type_display(),
            vehicle.get_status_display(),
            vehicle.total_revenue(),
            vehicle.total_maintenance_cost() + vehicle.total_fuel_cost(),
            round(vehicle.roi(), 2),
        ])
    
    return response

@login_required
def export_pdf(request):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title = Paragraph("FleetFlow Analytics Report", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Vehicle data
    data = [['Vehicle', 'Type', 'Status', 'Revenue', 'Costs', 'ROI %']]
    
    for vehicle in Vehicle.objects.all():
        data.append([
            vehicle.name,
            vehicle.get_vehicle_type_display(),
            vehicle.get_status_display(),
            f"₹{vehicle.total_revenue():.2f}",
            f"₹{vehicle.total_maintenance_cost() + vehicle.total_fuel_cost():.2f}",
            f"{vehicle.roi():.2f}%",
        ])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="fleet_analytics.pdf"'
    
    return response

@login_required
def chart_data(request):
    """API endpoint for chart data"""
    chart_type = request.GET.get('type', 'vehicle_status')
    
    if chart_type == 'vehicle_status':
        data = Vehicle.objects.values('status').annotate(count=Count('id'))
        return JsonResponse(list(data), safe=False)
    
    elif chart_type == 'monthly_revenue':
        # Last 6 months revenue
        data = []
        for i in range(6, 0, -1):
            month_start = timezone.now() - timedelta(days=30*i)
            month_end = timezone.now() - timedelta(days=30*(i-1))
            revenue = Trip.objects.filter(
                status='COMPLETED',
                completion_date__gte=month_start,
                completion_date__lt=month_end
            ).aggregate(total=Sum('revenue'))['total'] or 0
            
            data.append({
                'month': month_start.strftime('%b'),
                'revenue': float(revenue)
            })
        
        return JsonResponse(data, safe=False)
    
    return JsonResponse({'error': 'Invalid chart type'}, status=400)
