from django.urls import path
from . import views

urlpatterns = [
    path('', views.workshop_list, name='workshop_list'),
    path('<int:workshop_id>/', views.workshop_detail, name='workshop_detail'),
    path('dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('dashboard/add-service/', views.add_service, name='add_service'),
    path('dashboard/toggle-service/<int:service_id>/', views.toggle_service, name='toggle_service'),
    path('dashboard/delete-service/<int:service_id>/', views.delete_service, name='delete_service')
]