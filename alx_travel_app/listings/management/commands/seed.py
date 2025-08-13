import random
from decimal import Decimal
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

from listings.models import Listing, Booking, Review, BookingChoice, RoleChoice

User = get_user_model()


SAMPLE_LISTINGS = [
    {
        "title": "Stone Town Seafront Bungalow",
        "description": "Charming seafront bungalow with ocean views and easy access to the Stone Town nightlife.",
        "location": "Stone Town, Zanzibar, Tanzania",
        "price_per_night": Decimal("120.00"),
        "max_guests": 4,
    },
    {
        "title": "Table Mountain View Apartment",
        "description": "Modern 1-bedroom apartment with spectacular views of Table Mountain and quick access to the V&A Waterfront.",
        "location": "Cape Town, South Africa",
        "price_per_night": Decimal("90.00"),
        "max_guests": 2,
    },
    {
        "title": "Serengeti Mobile Safari Camp (All Inclusive)",
        "description": "Authentic mobile camp experience in the Serengeti. Includes game drives and local meals.",
        "location": "Serengeti, Tanzania",
        "price_per_night": Decimal("250.00"),
        "max_guests": 6,
    },
    {
        "title": "Lagos Boutique Loft",
        "description": "Stylish loft in Ikeja — close to business districts and nightlife. Fast Wi-Fi and secure building.",
        "location": "Ikeja, Lagos, Nigeria",
        "price_per_night": Decimal("70.00"),
        "max_guests": 3,
    },
    {
        "title": "Kente Homestay",
        "description": "Stay with local artisans in Kumasi. Learn about Kente weaving and local cuisine.",
        "location": "Kumasi, Ghana",
        "price_per_night": Decimal("50.00"),
        "max_guests": 3,
    },
    {
        "title": "Marrakech Traditional Riad",
        "description": "Beautiful riad in the Medina with interior courtyard, traditional decor and rooftop terrace.",
        "location": "Marrakech, Morocco",
        "price_per_night": Decimal("110.00"),
        "max_guests": 4,
    },
    {
        "title": "Westlands Short-stay Studio",
        "description": "Cozy studio close to restaurants and tech hubs. Great for business travellers.",
        "location": "Westlands, Nairobi, Kenya",
        "price_per_night": Decimal("60.00"),
        "max_guests": 2,
    },
    {
        "title": "Kigali Hills Cottage",
        "description": "Quiet cottage on the hills with a beautiful garden — ideal for a peaceful getaway.",
        "location": "Kimironko, Kigali, Rwanda",
        "price_per_night": Decimal("65.00"),
        "max_guests": 4,
    },
    {
        "title": "Riverside Guesthouse",
        "description": "Guesthouse near the river, family friendly, home-cooked breakfast available.",
        "location": "Kololo, Kampala, Uganda",
        "price_per_night": Decimal("55.00"),
        "max_guests": 3,
    },
    {
        "title": "Bakau Beach Hut",
        "description": "Simple beach hut steps from the sand — perfect for budget travelers who love the sea.",
        "location": "Bakau, The Gambia",
        "price_per_night": Decimal("40.00"),
        "max_guests": 2,
    },
]

AGENTS = [
    {"username": "musa_k", "email": "musa.k@uganda.demo.com", "first_name": "Musa", "last_name": "Kato", "phone": "+256772000001"},
    {"username": "nana_b", "email": "nana.b@ghana.demo.com", "first_name": "Nana", "last_name": "Boateng", "phone": "+233244000002"},
    {"username": "amina_s", "email": "amina.s@kenya.demo.com", "first_name": "Amina", "last_name": "Suleiman", "phone": "+254711000003"},
]

TRAVELERS = [
    {"username": "ada_n", "email": "ada.n@lagos.demo.com", "first_name": "Ada", "last_name": "Nwankwo"},
    {"username": "kwame_m", "email": "kwame.m@accra.demo.com", "first_name": "Kwame", "last_name": "Mensah"},
    {"username": "zola_m", "email": "zola.m@capetown.demo.com", "first_name": "Zola", "last_name": "Mbeki"},
    {"username": "mohammed_y", "email": "mohammed.y@rabat.demo.com", "first_name": "Mohammed", "last_name": "Youssef"},
    {"username": "priya_p", "email": "priya.p@nairobi.demo.com", "first_name": "Priya", "last_name": "Patel"},
    {"username": "thabo_s", "email": "thabo.s@johannesburg.demo.com", "first_name": "Thabo", "last_name": "Sizwe"},
]


REVIEW_COMMENTS = [
    "Amazing stay — host was welcoming and the location was perfect.",
    "Comfortable and clean; would definitely return.",
    "Great value for money. Local experience was unforgettable.",
    "Nice place but wifi could be improved.",
    "Exceptional hospitality and beautiful surroundings.",
]


class Command(BaseCommand):
    help = "Seed the DB with authentic African Listings, Bookings and Reviews."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Clearing existing Booking / Review / Listing data..."))
        #User.objects.all().delete()
        Booking.objects.all().delete()
        Review.objects.all().delete()
        Listing.objects.all().delete()

        # Create agents (hosts)
        agents = []
        for a in AGENTS:
            user, created = User.objects.get_or_create(
                email=a["email"],
                defaults={
                    "username": a["username"],
                    "first_name": a["first_name"],
                    "last_name": a["last_name"],
                    "phone": a.get("phone", ""),
                    "role": RoleChoice.AGENT,
                },
            )
            if created:
                # set a usable password for quick dev access
                user.set_password("password123")
                user.save()
            else:
                # make sure role is agent
                user.role = RoleChoice.AGENT
                user.save()
            agents.append(user)

        # Create travelers
        travelers = []
        for t in TRAVELERS:
            user, created = User.objects.get_or_create(
                email=t["email"],
                defaults={
                    "username": t["username"],
                    "first_name": t["first_name"],
                    "last_name": t["last_name"],
                    "role": RoleChoice.TRAVELER,
                },
            )
            if created:
                user.set_password("password123")
                user.save()
            travelers.append(user)

        # Create listings, assign agents round-robin
        self.stdout.write(self.style.WARNING("Creating listings..."))
        listings = []
        for idx, item in enumerate(SAMPLE_LISTINGS):
            agent = agents[idx % len(agents)]
            listing = Listing.objects.create(
                agent=agent,
                title=item["title"],
                description=item["description"],
                location=item["location"],
                price_per_night=item["price_per_night"],
                max_guests=item["max_guests"],
            )
            listings.append(listing)

        # Create bookings
        self.stdout.write(self.style.WARNING("Creating bookings..."))
        bookings_created = []
        for _ in range(30):
            listing = random.choice(listings)
            traveler = random.choice(travelers)

            nights = random.randint(1, 7)
            start_dt = timezone.now() + timedelta(days=random.randint(1, 30), hours=random.randint(0, 12))
            check_in = start_dt
            check_out = start_dt + timedelta(days=nights)

            # ensure num_of_traveler <= max_guests
            num_of_traveler = random.randint(1, listing.max_guests)

            total_price = listing.price_per_night * Decimal(nights)

            status = random.choice([BookingChoice.PENDING, BookingChoice.CONFIRMED, BookingChoice.CANCELLED])

            b = Booking.objects.create(
                traveler=traveler,
                listing=listing,
                num_of_traveler=num_of_traveler,
                check_in=check_in,
                check_out=check_out,
                total_price=total_price,
                status=status,
            )
            bookings_created.append(b)

        # Create reviews for some confirmed bookings (simulate guests leaving reviews)
        self.stdout.write(self.style.WARNING("Creating reviews for some confirmed bookings..."))
        confirmed = [b for b in bookings_created if b.status == BookingChoice.CONFIRMED]
        for b in confirmed:
            if random.random() < 0.6:  # ~60% of confirmed bookings have reviews
                rating = random.randint(3, 5)
                comment = random.choice(REVIEW_COMMENTS)
                Review.objects.create(
                    reviewer=b.traveler,
                    listing=b.listing,
                    rating=rating,
                    comment=comment,
                )

        self.stdout.write(self.style.SUCCESS("✅ Seeding complete: Listings, Bookings and Reviews created."))
        self.stdout.write(self.style.SUCCESS(f"Listings: {len(listings)} | Bookings: {len(bookings_created)} | Reviews: {Review.objects.count()}"))