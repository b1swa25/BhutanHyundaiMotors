from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from catalog.models import Part
from services.models import ServiceType
from .models import Announcement, SuccessStory

def home(request):
    featured_parts = Part.objects.all().order_by('-created_at')[:3]
    services = ServiceType.objects.all()
    announcement = Announcement.objects.filter(active=True).first()
    success_stories = SuccessStory.objects.filter(active=True).order_by('-created_at')
    return render(request, 'core/home.html', {
        'featured_parts': featured_parts,
        'services': services,
        'announcement': announcement,
        'success_stories': success_stories
    })

@login_required
def update_announcement(request):
    if request.user.role != 'ADMIN':
        messages.error(request, "Access denied.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        text = request.POST.get('announcement_text')
        is_active = request.POST.get('is_active') == 'on'
        
        # Deactivate all if this one is active
        if is_active:
            Announcement.objects.all().update(active=False)
            
        Announcement.objects.create(text=text, active=is_active)
        messages.success(request, "Announcement published successfully!")
    
    return redirect('dashboard')

@login_required
def create_success_story(request):
    if request.user.role != 'ADMIN':
        messages.error(request, "Access denied.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        customer_name = request.POST.get('customer_name')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        SuccessStory.objects.create(
            title=title,
            customer_name=customer_name,
            content=content,
            image=image
        )
        messages.success(request, "Success story added!")
    
    return redirect('dashboard')

@login_required
def delete_success_story(request, pk):
    if request.user.role != 'ADMIN':
        messages.error(request, "Access denied.")
        return redirect('dashboard')
    
    story = SuccessStory.objects.get(pk=pk)
    story.delete()
    messages.success(request, "Success story deleted.")
    return redirect('dashboard')

def custom_404(request, exception):
    """Custom 404 error handler"""
    return render(request, '404.html', status=404)
