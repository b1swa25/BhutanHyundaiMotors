import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bhutan_hyundai_motors.settings')
django.setup()

from catalog.models import Category, Part
from services.models import ServiceType
from users.models import CustomUser

from datetime import timedelta

def seed():
    # 1. Create Superuser if doesn't exist
    if not CustomUser.objects.filter(username='admin').exists():
        CustomUser.objects.create_superuser('admin', 'admin@example.com', 'admin123', role='ADMIN')
        print("Superuser created: admin / admin123")

    # 2. Create Categories
    categories = ['Electrical Components', 'Batteries', 'Lighting', 'Wiring & Connectors', 'Engine Spare Parts']
    for cat_name in categories:
        Category.objects.get_or_create(name=cat_name)

    # 3. Create Service Types
    services = [
        ('Battery Health Check', 'Complete diagnostic of battery health and charging system.', timedelta(minutes=30), 500),
        ('Wiring Repair', 'Professional repair of damaged or frayed vehicle wiring.', timedelta(hours=2), 1500),
        ('Alternator Service', 'Testing and repair of vehicle alternator.', timedelta(hours=1, minutes=30), 1200),
        ('Diagnostic Scan', 'Full OBD-II diagnostic scan for electrical faults.', timedelta(minutes=45), 800),
    ]
    for name, desc, dur, price in services:
        ServiceType.objects.get_or_create(
            name=name, 
            defaults={'description': desc, 'estimated_duration': dur, 'base_price': price}
        )
    
    # 4. Create some sample parts
    cat = Category.objects.get(name='Batteries')
    Part.objects.get_or_create(
        name='Exide Gold Maintenance Free Battery',
        defaults={
            'category': cat,
            'description': 'Premium maintenance-free battery for Japanese and Korean vehicles.',
            'price': 6500,
            'stock': 15,
            'added_by': CustomUser.objects.get(username='admin')
        }
    )

    print("Seeding complete!")

if __name__ == '__main__':
    seed()
