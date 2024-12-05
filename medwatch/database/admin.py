from django.contrib import admin
from .models import Measurement, Patient, Doctor, Sensor

# Register your models here.
admin.site.register(Measurement)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Sensor)