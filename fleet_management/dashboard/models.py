from django.db import models
from rest_framework import serializers

# Create your models here.
class Vehicle(models.Model):
    make  = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    

class Maintenance(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    date = models.DateField()
    details = models.TextField()

class Driver(models.Model):
    name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=100)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class Trip(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    distance = models.FloatField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    fuel_cost = models.FloatField()
    maintenance_required = models.BooleanField()

class FuelLog(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    fuel_date = models.DateField()
    fuel_type = models.CharField(max_length=100)
    fuel_quantity = models.FloatField()
    cost_per_unit = models.FloatField()
    total_cost = models.FloatField()