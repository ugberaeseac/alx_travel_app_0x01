import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from listings.models import User, Listing, Booking, Review, Role, BookingStatus
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = "Seed the database with sample data."

    def handle(self, *args, **kwargs):
        password = "test123"

        # Clear existing data
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()
        User.objects.all().delete()

        # Create users
        admin = User.objects.create(
            username="adminuser",
            email="admin@example.com",
            role=Role.ADMIN,
            password=make_password(password),
            is_superuser=True,
            is_staff=True
        )

        agents = []
        for i in range(2):
            agent = User.objects.create(
                username=f"agent{i}",
                email=f"agent{i}@example.com",
                role=Role.AGENT,
                password=make_password(password),
                is_staff=True
            )
            agents.append(agent)

        travelers = []
        for i in range(5):
            traveler = User.objects.create(
                username=f"traveler{i}",
                email=f"traveler{i}@example.com",
                role=Role.TRAVELER,
                password=make_password(password)
            )
            travelers.append(traveler)

        # Create listings
        listings = []
        for i in range(10):
            agent = random.choice(agents)
            start_date = timezone.now() + timedelta(days=i)
            end_date = start_date + timedelta(days=7)
            listing = Listing.objects.create(
                agent=agent,
                title=f"Trip {i}",
                description=f"Exciting tour number {i}",
                location=random.choice(["Nairobi", "Lagos", "Cairo", "Cape Town", "Accra"]),
                price=random.randint(100, 1000),
                start_date=start_date,
                end_date=end_date,
                available_slots=random.randint(1, 10),
            )
            listings.append(listing)

        # Create bookings
        for i in range(10):
            traveler = random.choice(travelers)
            listing = random.choice(listings)
            people = random.randint(1, 3)
            Booking.objects.create(
                traveller=traveler,
                listing=listing,
                number_of_people=people,
                status=random.choice(BookingStatus.values),
            )

        # Create reviews
        for i in range(10):
            traveler = random.choice(travelers)
            listing = random.choice(listings)
            Review.objects.create(
                traveller=traveler,
                listing=listing,
                rating=random.randint(1, 5),
                comment=f"This is review #{i} for {listing.title}."
            )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))

