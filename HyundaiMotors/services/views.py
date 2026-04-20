from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment, ServiceType
from .forms import AppointmentForm

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'services/book_appointment.html', {'form': form})

@login_required
def update_appointment_status(request, pk):
    if request.user.role != 'ADMIN':
        messages.error(request, "Access denied.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if not status:
            messages.error(request, "Status value is required.")
            return redirect('dashboard')
        
        try:
            appointment = Appointment.objects.get(pk=pk)
            appointment.status = status
            appointment.save()
            messages.success(request, f"Appointment status updated to {appointment.get_status_display()}.")
        except Appointment.DoesNotExist:
            messages.error(request, "Appointment not found.")
    
    return redirect('dashboard')
