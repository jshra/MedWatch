from django import forms
from .models import Measurement, Patient, Doctor, Sensor
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class DoctorRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=100)
    surname = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'name', 'surname', 'email', 'phone_number']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            doctor = Doctor(user=user, name=self.cleaned_data['name'], surname=self.cleaned_data['surname'],
                            email=self.cleaned_data['email'], phone_number=self.cleaned_data['phone_number'])
            doctor.save()
        return user
    
class SensorRegistrationForm(UserCreationForm):
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'patient']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            sensor = Sensor(user=user, patient=self.cleaned_data['patient'])
            sensor.save()
        return user

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['HR', 'saturation', 'temperature', 'patient']

class PatientForm(forms.ModelForm):
    csv_file = forms.FileField(required=False)

    class Meta:
        model = Patient
        fields = ['name', 'surname', 'doctor', 'csv_file']