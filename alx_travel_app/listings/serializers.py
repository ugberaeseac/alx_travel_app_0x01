from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Listing, Booking




class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

    def validate_max_guest(self, value):
        if value <= 0:
            raise ValidationError({'detail': 'The maximum number of guest must be greater than 0'})



class ListingSerializer(serializers.ModelSerializer):
    bookings = BookingSerializer(many=True, read_only=True)
    class Meta:
        model = Listing
        fields = '__all__'



