from django.db import models
from django.contrib.auth.models import User

class Workshop(models.Model):
    name = models.CharField(max_length=200)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='workshop')
    address = models.TextField()
    phone = models.CharField(max_length=20)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name