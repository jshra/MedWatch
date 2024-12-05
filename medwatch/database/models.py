from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} {self.surname}"

class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.patient_id}"

class Measurement(models.Model):
    id = models.AutoField(primary_key=True)
    HR = models.FloatField()
    saturation = models.FloatField()
    temperature = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)  # Automatically set to the current time
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    def __str__(self):
        return f"Measurement for {self.patient.name} at {self.timestamp}"
    
class Sensor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sensor_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='sensor')

    def __str__(self):
        return f"Sensor {self.sensor_id} for Patient {self.patient}"
    

