from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomerProfile, MechanicProfile, FrontDeskProfile
from bookings.models import Booking
from workshops.models import Workshop


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email    = request.POST['email']
        password = request.POST['password']
        phone    = request.POST['phone']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        CustomerProfile.objects.create(user=user, phone=phone)
        messages.success(request, 'Account created! Please log in.')
        return redirect('login')

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect based on role
            if hasattr(user, 'frontdeskprofile'):
                return redirect('frontdesk_dashboard')
            elif hasattr(user, 'mechanicprofile'):
                return redirect('technician_dashboard')
            elif hasattr(user, 'workshop'):
                return redirect('owner_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    try:
        customer_profile = CustomerProfile.objects.get(user=request.user)
    except CustomerProfile.DoesNotExist:
        customer_profile = CustomerProfile.objects.create(user=request.user)

    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name  = request.POST.get('last_name', '')
        request.user.email      = request.POST.get('email', '')
        request.user.save()
        customer_profile.phone = request.POST.get('phone', '')
        customer_profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    return render(request, 'accounts/profile.html', {
        'customer_profile': customer_profile,
    })


@login_required
def frontdesk_dashboard(request):
    # Make sure user is front desk
    if not hasattr(request.user, 'frontdeskprofile'):
        messages.error(request, 'Access denied.')
        return redirect('home')

    workshop = request.user.frontdeskprofile.workshop

    # Get all mechanics in this workshop
    mechanics = MechanicProfile.objects.filter(workshop=workshop)

    # Handle assignment
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        mechanic_id = request.POST.get('mechanic_id')
        booking = get_object_or_404(Booking, id=booking_id)
        mechanic = get_object_or_404(User, id=mechanic_id)
        booking.assigned_to = mechanic
        booking.status = 'assigned'
        booking.save()
        messages.success(request, f'Booking assigned to {mechanic.username}.')
        return redirect('frontdesk_dashboard')

    # Get all bookings for this workshop
    bookings = Booking.objects.filter(workshop=workshop).order_by('-created_at')

    return render(request, 'accounts/frontdesk_dashboard.html', {
        'workshop': workshop,
        'bookings': bookings,
        'mechanics': mechanics,
    })


@login_required
def technician_dashboard(request):
    # Make sure user is a mechanic
    if not hasattr(request.user, 'mechanicprofile'):
        messages.error(request, 'Access denied.')
        return redirect('home')

    # Get bookings assigned to this technician
    assigned_bookings = Booking.objects.filter(
        assigned_to=request.user
    ).order_by('-created_at')

    # Handle status update
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        new_status = request.POST.get('status')
        booking = get_object_or_404(Booking, id=booking_id, assigned_to=request.user)
        booking.status = new_status
        booking.save()
        messages.success(request, 'Job status updated.')
        return redirect('technician_dashboard')

    return render(request, 'accounts/technician_dashboard.html', {
        'bookings': assigned_bookings,
        'mechanic': request.user.mechanicprofile,
    })