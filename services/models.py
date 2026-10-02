from django.db import models
from workshops.models import Workshop

DEPARTMENT_CHOICES = [
    ('mechanical', 'Mechanical'),
    ('electrical', 'Electrical'),
    ('tyres', 'Tyres & Wheels'),
    ('ac_cooling', 'AC & Cooling'),
    ('body_paint', 'Body & Paint'),
    ('oils_fluids', 'Oils & Fluids'),
]

class Service(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='services')
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, default='mechanical')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.IntegerField(default=60)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.workshop.name})"