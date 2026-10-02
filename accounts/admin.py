from django.contrib import admin
from .models import CustomerProfile, MechanicProfile, FrontDeskProfile

admin.site.register(CustomerProfile)
admin.site.register(MechanicProfile)
admin.site.register(FrontDeskProfile)