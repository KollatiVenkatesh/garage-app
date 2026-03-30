from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('delete-customer/<int:id>/', views.delete_customer, name='delete_customer'),
    path('delete-vehicle/<int:id>/', views.delete_vehicle, name='delete_vehicle'),
    path('delete-visit/<int:id>/', views.delete_visit, name='delete_visit'),
    path('add-vehicle/', views.add_vehicle, name='add_vehicle'),
    path('add-visit/', views.add_visit, name='add_visit'),
    path('add-customer/', views.add_customer, name='add_customer'),
    path('vehicle/<int:vehicle_id>/', views.vehicle_history, name='vehicle_history'),
    path('add-repair/<int:visit_id>/', views.add_repair, name='add_repair'),
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('update-status/<int:job_id>/', views.update_status, name='update_status'),
]