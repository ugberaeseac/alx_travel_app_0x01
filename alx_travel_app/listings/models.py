from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
import uuid


class RoleChoice(models.TextChoices):
    TRAVELER = 'Traveler'
    AGENT = 'Agent'
    ADMIN = 'Admin'


class BookingChoice(models.TextChoices):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    CANCELLED = 'Cancelled'


class User(AbstractUser):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(max_length=10, choices=RoleChoice.choices, default=RoleChoice.TRAVELER)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.username} - {self.email} - {self.role}'



class Listing(models.Model):
    listing_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)
    location = models.CharField(max_length=100, null=False, blank=False)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    max_guests = models.PositiveIntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f'{self.title}'



class Booking(models.Model):
    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    traveler = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    num_of_traveler = models.PositiveIntegerField(null=False)
    check_in = models.DateTimeField() #start_date
    check_out = models.DateTimeField() #end_date
    #total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    status = models.CharField(max_length=10, choices=BookingChoice.choices, default=BookingChoice.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    @property
    def total_price(self):
        num_of_nights = (self.check_out.date() - self.check_in.date()).days
        if num_of_nights < 1:
            num_of_nights = 1
        return float(self.listing.price_per_night * num_of_nights)


    def __str__(self):
        return f' Booking {self.booking_id} by {self.traveler.username}'



class Review(models.Model):
    review_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(null=False)
    comment = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f'Review {self.rating}/5 by {self.reviewer.username}'



