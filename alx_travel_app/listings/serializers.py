from rest_framework import serializers
from .models import Listing, Booking


class ListingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Listing
        fields = (
                'listing_id',
                'agent',
                'title',
                'location',
                'price',
                'start_date',
                'end_date',
                'available_slots'
                )


class BookingSerializer(serializers.ModelSerializer):

    listing = ListingSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = (
                'booking_id',
                'traveller',
                'listing',
                'number_of_people',
                'status',
                'created_at'
                )
