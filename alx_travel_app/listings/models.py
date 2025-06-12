import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Role(models.TextChoices):
    TRAVELER = 'Traveler'
    AGENT = 'Agent'
    ADMIN = 'Admin'   


class User(AbstractUser):
    user_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField(unique=True, null=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=10, choices=Role.choices, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.email}, ({self.role})'



class Listing(models.Model):
    listing_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    location = models.CharField(max_length=255, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    available_slots = models.PositiveIntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_available(self):
        return self.available_slots > 0

    def __str__(self):
        return self.title


class BookingStatus(models.TextChoices):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    CANCELLED = 'Cancelled'


class Booking(models.Model):
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    traveller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    number_of_people = models.PositiveIntegerField(null=False)
    status = models.CharField(max_length=10, choices=BookingStatus.choices, null=False, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def total_price(self):
        return self.traveller.price * self.number_of_people


    def __str__(self):
        return f'Booking {self.booking_id} by {self.traveller.email}'


class Review(models.Model):
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    traveller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(null=False)
    comment = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('Rating must be between 1 and 5')

    def __str__(self):
        return f'Review {self.rating}/5 by {self.traveller.email}'


