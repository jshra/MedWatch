from django.shortcuts import render, redirect
from .forms import MeasurementForm, PatientForm, DoctorRegistrationForm
from .models import Measurement, Patient, Doctor
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Measurement, Patient
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import csv
from io import TextIOWrapper
from django.http import JsonResponse


def home(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Doctors').exists():
            return redirect('doctor_home')
        else:
            return render(request, 'database/unverified_login.html')
    return render(request, 'database/home.html')


@login_required
def doctor_home(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
        patients = Patient.objects.filter(doctor=doctor)
    except Doctor.DoesNotExist:
        patients = []

    context = {
        'patients': patients,
    }
    return render(request, 'database/doctor_home.html', context)

@login_required
def patient_measurements(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id, doctor__user=request.user)
    measurements = Measurement.objects.filter(patient=patient).order_by('timestamp')

    # Get filtering parameters from GET request
    hr_min = request.GET.get('hr_min')
    saturation_min = request.GET.get('saturation_min')
    temperature_min = request.GET.get('temperature_min')
    search_text = request.GET.get('search_text', '')

    # Apply filter
    if hr_min:
        measurements = measurements.filter(HR__gte=hr_min)
    if saturation_min:
        measurements = measurements.filter(saturation__gte=saturation_min)
    if temperature_min:
        measurements = measurements.filter(temperature__gte=temperature_min)

    # Pagination
    page = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 10)
    paginator = Paginator(measurements, per_page)

    measurements_page = paginator.get_page(page)

    context = {
        'patient': patient,
        'measurements': measurements_page,
        'page': page,
        'per_page': per_page,
        'num_pages': paginator.num_pages,
        'hr_min': hr_min,
        'saturation_min': saturation_min,
        'temperature_min': temperature_min,
        'search_text': search_text,
    }
    return render(request, 'database/patient_measurements.html', context)

@login_required
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            patient = form.save()
            csv_file = request.FILES.get('csv_file')

            if csv_file:
                file_data = TextIOWrapper(csv_file.file, encoding='utf-8')
                reader = csv.reader(file_data)

                # Skip the header row if it exists
                next(reader, None)

                # Process the CSV data
                for row in reader:
                    Measurement.objects.create(
                        patient=patient,
                        HR=row[0],
                        saturation=row[1],
                        temperature=row[2],
                        timestamp=row[3]
                    )

            return redirect('patients_list')
    else:
        form = PatientForm()

    return render(request, 'database/add_patient.html', {'form': form})



@csrf_exempt
def add_measurement(request):
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'}, status=201)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'database/doctor_list.html', {'doctors': doctors})

def patients_list(request):
    patients = Patient.objects.all()
    return render(request, 'database/patients_list.html', {'patients': patients})

def register(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('unverified_login')
    else:
        form = DoctorRegistrationForm()
    return render(request, 'database/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'database/login.html', {'form': form})
