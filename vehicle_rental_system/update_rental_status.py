
from django.core.management.base import BaseCommand
from django.utils import timezone
from models import Rental  
import schedule
import time

class Command(BaseCommand):
    help = 'Updates the status of rentals based on the end date using schedule'

    def handle(self, *args, **kwargs):
        schedule.every().day.at("00:00").do(self.update_rental_statuses)

        while True:
            schedule.run_pending()
            time.sleep(60)  

    def update_rental_statuses(self):
        now = timezone.now()
        expired_rentals = Rental.objects.filter(RentalEndDateTime__lt=now, status__in=["Pending", "Ongoing", "Confirm"])

        for rental in expired_rentals:
            rental.status = "Expired"
            rental.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated rental {rental.id} to Expired'))
