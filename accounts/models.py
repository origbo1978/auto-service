from django.db import models
from django.contrib.auth.models import User

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username


class MechanicProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    workshop = models.ForeignKey('workshops.Workshop', on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=20, blank=True)
    specialization = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


class FrontDeskProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    workshop = models.ForeignKey('workshops.Workshop', on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username