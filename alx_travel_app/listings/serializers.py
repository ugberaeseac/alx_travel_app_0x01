from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User, Listing, Booking, Review
from datetime import datetime


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=50, write_only=True)
    class Meta:
        model = User
        fields = '__all__'



class BookingSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    check_in = serializers.DateTimeField(input_formats=['%d/%m/%Y'], format="%d/%m/%Y")
    check_out = serializers.DateTimeField(input_formats=['%d/%m/%Y'], format="%d/%m/%Y")

    class Meta:
        model = Booking
        fields = '__all__'

    def validate_num_of_traveler(self, value):
        if value <= 0:
            raise ValidationError({'detail': 'The number of travelers must be greater than 0'})
        return value



class ListingSerializer(serializers.ModelSerializer):
    bookings = BookingSerializer(many=True, read_only=True)
    class Meta:
        model = Listing
        fields = '__all__'

    def validate_max_guests(self, value):
        if value <= 0:
            raise ValidationError({'detail': 'The maximum number of guest must be greater than 0'})
        return value


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise ValidationError({'detail': 'Rating must be between 1 and 5'})
        return value



