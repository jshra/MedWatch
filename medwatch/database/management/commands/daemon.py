from django.conf import settings
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from database.models import Measurement, Patient
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

def my_job():
    patients = Patient.objects.all()

    for patient in patients:
        latest_measurement = Measurement.objects.filter(patient=patient).order_by('-timestamp').first()

        if latest_measurement:
            if (latest_measurement.HR is not None and latest_measurement.HR > 1000) or \
               (latest_measurement.saturation is not None and latest_measurement.saturation > 1000) or \
               (latest_measurement.temperature is not None and latest_measurement.temperature > 1000):

                doctor_email = patient.doctor.user.email
                subject = f"Low measurement values alert for patient {patient.name} {patient.surname}"
                message = f"Dear Dr. {patient.doctor.surname},\n\n" \
                          f"This is to inform you that the latest measurement values for patient {patient.name} {patient.surname} " \
                          f"are not in the acceptable thresholds.\n\n" \
                          f"Please take appropriate action.\n\n" \
                          f"Thank you."
                
                send_mail(subject, message, 'jshutyra@gmail.com', [doctor_email])

                print(f"Email sent to {doctor_email} for patient {patient.name} {patient.surname}")
            else:
                print(f"No action needed for patient {patient.name} {patient.surname}")

        else:
            print(f"No measurements found for patient {patient.name} {patient.surname}")

@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
        my_job,
        trigger=CronTrigger(minute="*"),  # Every 10 seconds
        id="my_job",  # The `id` assigned to each job MUST be unique
        max_instances=1,
        replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(
            day_of_week="mon", hour="00", minute="00"
        ),  # Midnight on Monday, before start of the next work week.
        id="delete_old_job_executions",
        max_instances=1,
        replace_existing=True,
        )
        logger.info(
        "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")