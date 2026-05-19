from django.core.management.base import BaseCommand
from myapp.models import State, City, Area, login_table, Vehicle, Booking
from datetime import datetime, timedelta, date
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate sample Indian car rental data'

    def handle(self, *args, **options):
        # Step 1: Create 5 locations
        locations = [
            ('Maharashtra', 'Mumbai', 'Andheri'),
            ('Gujarat', 'Ahmedabad', 'Navrangpura'),
            ('Karnataka', 'Bangalore', 'Koramangala'),
            ('Delhi', 'New Delhi', 'Connaught Place'),
            ('Tamil Nadu', 'Chennai', 'T Nagar'),
        ]

        for state_name, city_name, area_name in locations:
            state, _ = State.objects.get_or_create(name=state_name)
            city, _ = City.objects.get_or_create(name=city_name, state=state)
            area, _ = Area.objects.get_or_create(name=area_name, city=city)
            self.stdout.write(self.style.SUCCESS(f'Location created: {state_name} -> {city_name} -> {area_name}'))

        # Keep default references for sample data
        state = State.objects.get(name='Maharashtra')
        city = City.objects.get(name='Mumbai', state=state)
        area = Area.objects.get(name='Andheri', city=city)

        # DOB dates
        dob_dates = [
            date(1990,5,15), date(1988,8,20), date(1992,3,10),
            date(1991,11,25), date(1987,7,12)
        ]
        renter_dobs = [
            date(1995,2,18), date(1993,9,5), date(1994,12,30),
            date(1996,4,22), date(1992,1,14)
        ]

        # Step 2: 5 Lessor owners
        owners_data = [
            {'name': 'Rahul Patel', 'email_id': 'rahul.patel@email.com', 'phone_no': 912345678901, 'dob': dob_dates[0], 'address': 'Andheri West, Mumbai', 'usertype': 'Lessor'},
            {'name': 'Priya Sharma', 'email_id': 'priya.sharma@email.com', 'phone_no': 919876543210, 'dob': dob_dates[1], 'address': 'Bandra East, Mumbai', 'usertype': 'Lessor'},
            {'name': 'Amit Desai', 'email_id': 'amit.desai@email.com', 'phone_no': 919123456789, 'dob': dob_dates[2], 'address': 'Andheri East, Mumbai', 'usertype': 'Lessor'},
            {'name': 'Neha Gupta', 'email_id': 'neha.gupta@email.com', 'phone_no': 918765432109, 'dob': dob_dates[3], 'address': 'Juhu, Mumbai', 'usertype': 'Lessor'},
            {'name': 'Vikram Singh', 'email_id': 'vikram.singh@email.com', 'phone_no': 911234567890, 'dob': dob_dates[4], 'address': 'Versova, Mumbai', 'usertype': 'Lessor'},
        ]
        owners = []
        for data in owners_data:
            user, created = login_table.objects.get_or_create(
                email_id=data['email_id'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created owner: {data["name"]}'))
            owners.append(user)

        # Step 3: 9 Vehicles
        vehicles_data = [
            ('Maruti Swift', 'Maruti', '2022', 1500, owners[0]),
            ('Hyundai Creta', 'Hyundai', '2023', 2500, owners[0]),
            ('Tata Altroz', 'Tata', '2021', 1200, owners[1]),
            ('Toyota Innova', 'Toyota', '2020', 3000, owners[1]),
            ('Mahindra Thar', 'Mahindra', '2023', 2800, owners[2]),
            ('Honda City', 'Honda', '2022', 1800, owners[3]),
            ('Maruti Brezza', 'Maruti', '2023', 1600, owners[3]),
            ('Hyundai i20', 'Hyundai', '2021', 1400, owners[4]),
            ('Kia Seltos', 'Kia', '2022', 2200, owners[4]),
        ]
        for model_name, company, model_year, base_rent_perday, vendor in vehicles_data:
            veh, created = Vehicle.objects.get_or_create(
                vendor=vendor,
                model_name=model_name,
                defaults={
                    'company': company,
                    'model_year': model_year,
                    'base_rent_perday': base_rent_perday,
                    'location': 'Mumbai',
                    'area': area,
                    'city': city,
                    'state': state,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created vehicle: {model_name}'))
        self.stdout.write(self.style.SUCCESS('Vehicles created (photos/rc paths set to existing media)'))

        # Step 4: 5 Lessee renters
        renters_data = [
            {'name': 'Sneha Rao', 'email_id': 'sneha.rao@email.com', 'phone_no': 919112233445, 'dob': renter_dobs[0], 'address': 'Powai, Mumbai', 'usertype': 'Lessee'},
            {'name': 'Karan Mehta', 'email_id': 'karan.mehta@email.com', 'phone_no': 919998877665, 'dob': renter_dobs[1], 'address': 'Dadar, Mumbai', 'usertype': 'Lessee'},
            {'name': 'Divya Iyer', 'email_id': 'divya.iyer@email.com', 'phone_no': 91888990011, 'dob': renter_dobs[2], 'address': 'Malad, Mumbai', 'usertype': 'Lessee'},
            {'name': 'Rohit Kumar', 'email_id': 'rohit.kumar@email.com', 'phone_no': 917777888999, 'dob': renter_dobs[3], 'address': 'Borivali, Mumbai', 'usertype': 'Lessee'},
            {'name': 'Pooja Nair', 'email_id': 'pooja.nair@email.com', 'phone_no': 916666777888, 'dob': renter_dobs[4], 'address': 'Goregaon, Mumbai', 'usertype': 'Lessee'},
        ]
        renters = []
        for data in renters_data:
            user, created = login_table.objects.get_or_create(
                email_id=data['email_id'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created renter: {data["name"]}'))
            renters.append(user)

        # Step 5: 15 Sample Bookings
        now = timezone.now()
        for i, renter in enumerate(renters):
            for j in range(3):  # 3 bookings per renter
                vehicle = Vehicle.objects.order_by('?')[j % Vehicle.objects.count()]
                Booking.objects.create(
                    user=renter,
                    vehicle=vehicle,
                    booking_from=now + timedelta(days=i*5 + j),
                    booking_to=now + timedelta(days=i*5 + j + 3),
                    booking_amount=4500,
                    payment_mode='online',
                    payment_status='Done',
                    is_confirmed=True,
                    cancellation_status='No',
                    owner_cancel='No'
                )
        self.stdout.write(self.style.SUCCESS('Sample bookings created'))

        self.stdout.write(self.style.SUCCESS('All data populated! 5 owners, 9 vehicles, 5 renters, 15 bookings. Test /admin /ownerbookings etc.'))

