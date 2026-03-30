from django.db import models
from django.utils import timezone

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    # address = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Vehicle(models.Model):
    number_plate = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.number_plate


class Visit(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    notes = models.CharField(max_length=255)
    km_reading = models.IntegerField()   # 🔥 NEW FIELD
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle.number_plate} - {self.created_at}"


class RepairJob(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    job_type = models.CharField(max_length=100)
    cost = models.FloatField()
    status = models.CharField(
        choices=[('Pending', 'Pending'), ('Completed', 'Completed')],
        max_length=10
    )
    updated_at = models.DateTimeField(auto_now=True)  # 🔥 NEW FIELD

    def __str__(self):
        return self.job_type
    def __str__(self):
        return self.job_type