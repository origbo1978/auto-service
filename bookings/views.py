import os
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from services.models import Service
from .models import Booking, ISSUE_CATEGORIES

BREVO_API_KEY = os.environ.get('BREVO_API_KEY', '')

def send_booking_email(to_email, username, service, booking_date, booking_time):
    try:
        requests.post(
            'https://api.brevo.com/v3/smtp/email',
            headers={
                'api-key': BREVO_API_KEY,
                'Content-Type': 'application/json',
            },
            json={
                'sender': {'name': 'AutoServe NG', 'email': 'legendskye124@gmail.com'},
                'to': [{'email': to_email}],
                'subject': 'Booking Confirmed — AutoServe NG',
                'textContent': f'''Hi {username},

Your booking has been received successfully!

Service:  {service.name}
Workshop: {service.workshop.name}
Address:  {service.workshop.address}
Date:     {booking_date}
Time:     {booking_time}
Price:    ₦{service.price}

You can track your booking status by logging into AutoServe NG.

Thank you for choosing AutoServe NG!
'''
            }
        )
    except Exception:
        pass


@login_required
def booking_list(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})


@login_required
def booking_create(request):
    service_id = request.GET.get('service')
    service = Service.objects.get(id=service_id)

    if request.method == 'POST':
        booking_date     = request.POST['booking_date']
        booking_time     = request.POST['booking_time']
        notes            = request.POST.get('notes', '')
        issue_category   = request.POST.get('issue_category', '')

        Booking.objects.create(
            customer=request.user,
            workshop=service.workshop,
            service=service,
            booking_date=booking_date,
            booking_time=booking_time,
            notes=notes,
            issue_category=issue_category,
        )

        send_booking_email(
            to_email=request.user.email,
            username=request.user.username,
            service=service,
            booking_date=booking_date,
            booking_time=booking_time,
        )

        messages.success(request, 'Booking confirmed! A confirmation email has been sent.')
        return redirect('booking_list')

    return render(request, 'bookings/booking_create.html', {
        'service': service,
        'issue_categories': ISSUE_CATEGORIES,
    })


@login_required
def update_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.workshop.owner != request.user:
        messages.error(request, 'You are not allowed to do that.')
        return redirect('owner_dashboard')
    if request.method == 'POST':
        new_status = request.POST['status']
        booking.status = new_status
        booking.save()
        messages.success(request, f'Status updated to {booking.get_status_display()}.')
    return redirect('owner_dashboard')


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    if booking.status in ['pending', 'assigned']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Your booking has been cancelled.')
    else:
        messages.error(request, 'This booking cannot be cancelled at this stage.')
    return redirect('booking_list')