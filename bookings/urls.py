from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_list, name='booking_list'),
    path('create/', views.booking_create, name='booking_create'),
    path('update-status/<int:booking_id>/', views.update_status, name='update_status'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]