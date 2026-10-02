from django.shortcuts import render
from workshops.models import Workshop

def home(request):
    workshops = Workshop.objects.all()[:3]
    return render(request, 'home.html', {'workshops': workshops})