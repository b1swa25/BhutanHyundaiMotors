from django.db import models
from django.conf import settings

class ServiceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    estimated_duration = models.DurationField(help_text="HH:MM:SS")
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reference_number = models.CharField(max_length=50, unique=True, blank=True)
    next_service_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def status_choices(self):
        return [
            {'value': val, 'label': lbl, 'selected': self.status == val}
            for val, lbl in self.STATUS_CHOICES
        ]

    def save(self, *args, **kwargs):
        if not self.reference_number:
            import datetime
            prefix = "BHM"
            today = datetime.date.today()
            date_str = today.strftime("%Y%m%d")
            
            # Count how many appointments already exist for today
            day_count = Appointment.objects.filter(created_at__date=today).count()
            sequence = str(day_count + 1).zfill(4)
            
            self.reference_number = f"{prefix}-{date_str}-{sequence}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.service_type} on {self.date}"

    @property
    def whatsapp_admin_link(self):
        from .utils import generate_whatsapp_link
        from django.conf import settings
        message = f"Hi Admin, I have booked a {self.service_type.name} service for {self.date} at {self.time}. My username is {self.user.username}. Please confirm my appointment."
        return generate_whatsapp_link(settings.ADMIN_WHATSAPP_NUMBER, message)

    @property
    def whatsapp_customer_link(self):
        from .utils import generate_whatsapp_link
        if not self.user.phone:
            return None
        # Clean phone number (remove +, spaces, etc.)
        phone = ''.join(filter(str.isdigit, self.user.phone))
        message = f"Hello {self.user.username}! Your {self.service_type.name} service at Bhutan Hyundai Motors is now {self.get_status_display()} for {self.date} at {self.time}. Thank you!"
        return generate_whatsapp_link(phone, message)
