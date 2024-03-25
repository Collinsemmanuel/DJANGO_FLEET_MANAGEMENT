from django.contrib import admin

# Register your models here.
from .import *
admin.site.register(Vehicle)
admin.site.register(Maintenance)
admin.site.register(Driver)
admin.site.register(Trip)
admin.site.register(FuelLog)
