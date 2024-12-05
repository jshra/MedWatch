from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from .models import Measurement, Patient
from django.core.mail import send_mail
from django.utils import timezone

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

def send_measurement_alerts():
    print('hello')

# Add your job to the scheduler
scheduler.add_job(send_measurement_alerts, trigger='interval', minutes=1)

# Start the scheduler
scheduler.start()