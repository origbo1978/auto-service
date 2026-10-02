from django.db import models
from django.contrib.auth.models import User
from workshops.models import Workshop
from services.models import Service

ISSUE_CATEGORIES = [
    ('engine', 'Engine Problems'),
    ('ac', 'AC & Cooling Issues'),
    ('brakes', 'Brake Problems'),
    ('electrical', 'Electrical Issues'),
    ('tyres', 'Tyre & Wheel Issues'),
    ('body', 'Body & Paint Damage'),
    ('oils', 'Oil & Fluid Issues'),
    ('starting', 'Car Not Starting'),
    ('noise', 'Unusual Noise'),
    ('other', 'Other Issue'),
]

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_bookings')
    booking_date = models.DateField()
    booking_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    issue_category = models.CharField(max_length=20, choices=ISSUE_CATEGORIES, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} - {self.service.name}"