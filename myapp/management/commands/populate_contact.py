
from django.core.management.base import BaseCommand
from myapp.models import Contactus

class Command(BaseCommand):
    help = 'Populate sample contact data'

    def handle(self, *args, **options):
        contacts = [
            {'name': 'John Doe', 'email': 'john@example.com', 'subject': 'Car inquiry', 'message': 'Interested in Maruti Swift.'},
            {'name': 'Jane Smith', 'email': 'jane@test.com', 'subject': 'Booking issue', 'message': 'Cancel booking ID 1.'},
            {'name': 'Bob Johnson', 'email': 'bob@real.com', 'subject': 'Price quote', 'message': 'Hyundai Creta weekend rate?'},
        ]
        for data in contacts:
            Contactus.objects.get_or_create(
                email=data['email'],
                defaults=data
            )
        self.stdout.write(self.style.SUCCESS('3 sample contact records created'))

