from django.urls import path
from .views import home, VehicleList

urlpatterns = [
    path('', home, name='dashboard-home'),
    path('vehicles/', VehicleList.as_view(), name='vehicle-list'),
]