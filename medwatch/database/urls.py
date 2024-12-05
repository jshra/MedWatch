from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('add/', views.add_measurement, name='add_measurement'),
    path('patients/list/', views.patients_list, name='patients_list'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('doctor_home/', views.doctor_home, name='doctor_home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('patients/<int:patient_id>/', views.patient_measurements, name='patient_measurements'),
    path('add_measurement/', views.add_measurement, name='add_measurement'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    #path('register_sensor/', views.register_sensor, name='register_sensor'),
    #path('sensor_home/', views.sensor_home, name='sensor_home'),
]