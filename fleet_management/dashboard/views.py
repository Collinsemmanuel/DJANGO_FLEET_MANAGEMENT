from django.shortcuts import render
from .models import Vehicle, Maintenance, Driver
from django.http import HttpResponse
from .serializers import VehicleSerializer
from rest_framework import generics
from django.views.generic import ListView

class VehicleList(ListView):
    model = Vehicle
    template_name = 'dashboard/vehicle_list.html'  # Specify your template name here

def home(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'dashboard/home.html', {'vehicles': vehicles})