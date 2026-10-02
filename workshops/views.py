from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .models import Workshop
from services.models import Service, DEPARTMENT_CHOICES
from bookings.models import Booking

def workshop_list(request):
    query = request.GET.get('q', '')
    workshops = Workshop.objects.all()
    if query:
        workshops = workshops.filter(
            models.Q(name__icontains=query) |
            models.Q(address__icontains=query)
        )
    return render(request, 'workshops/workshop_list.html', {
        'workshops': workshops,
        'query': query,
    })

def workshop_detail(request, workshop_id):
    workshop = get_object_or_404(Workshop, id=workshop_id)
    selected_dept = request.GET.get('dept', None)
    
    # Build departments that have at least one available service
    departments = []
    for key, label in DEPARTMENT_CHOICES:
        services = Service.objects.filter(
            workshop=workshop,
            department=key,
            is_available=True
        )
        if services.exists():
            departments.append({
                'key': key,
                'label': label,
                'count': services.count(),
            })

    # If a department is selected show its services
    selected_services = []
    selected_dept_label = None
    if selected_dept:
        selected_services = Service.objects.filter(
            workshop=workshop,
            department=selected_dept,
            is_available=True
        )
        selected_dept_label = dict(DEPARTMENT_CHOICES).get(selected_dept, '')

    return render(request, 'workshops/workshop_detail.html', {
        'workshop': workshop,
        'departments': departments,
        'selected_dept': selected_dept,
        'selected_dept_label': selected_dept_label,
        'selected_services': selected_services,
    })

@login_required
def owner_dashboard(request):
    try:
        workshop = Workshop.objects.get(owner=request.user)
    except Workshop.DoesNotExist:
        messages.error(request, 'You do not have a workshop assigned.')
        return redirect('home')

    bookings = Booking.objects.filter(workshop=workshop).order_by('-created_at')
    services = Service.objects.filter(workshop=workshop)

    return render(request, 'workshops/owner_dashboard.html', {
        'workshop': workshop,
        'bookings': bookings,
        'services': services,
        'department_choices': DEPARTMENT_CHOICES,
    })

@login_required
def add_service(request):
    try:
        workshop = Workshop.objects.get(owner=request.user)
    except Workshop.DoesNotExist:
        messages.error(request, 'You do not have a workshop assigned.')
        return redirect('home')

    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST.get('description', '')
        price = request.POST['price']
        duration = request.POST['duration_minutes']
        department = request.POST['department']

        Service.objects.create(
            workshop=workshop,
            name=name,
            description=description,
            price=price,
            duration_minutes=duration,
            department=department,
        )
        messages.success(request, 'Service added successfully!')
        return redirect('owner_dashboard')

    return render(request, 'workshops/add_service.html', {
        'workshop': workshop,
        'department_choices': DEPARTMENT_CHOICES,
    })

@login_required
def toggle_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if service.workshop.owner != request.user:
        messages.error(request, 'You are not allowed to do that.')
        return redirect('owner_dashboard')
    service.is_available = not service.is_available
    service.save()
    status = 'available' if service.is_available else 'unavailable'
    messages.success(request, f'{service.name} is now {status}.')
    return redirect('owner_dashboard')

@login_required
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if service.workshop.owner != request.user:
        messages.error(request, 'You are not allowed to do that.')
        return redirect('owner_dashboard')
    if request.method == 'POST':
        service_name = service.name
        service.delete()
        messages.success(request, f'{service_name} has been deleted.')
    return redirect('owner_dashboard')