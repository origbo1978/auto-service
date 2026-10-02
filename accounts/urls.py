from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('frontdesk/', views.frontdesk_dashboard, name='frontdesk_dashboard'),
    path('technician/', views.technician_dashboard, name='technician_dashboard'),
]