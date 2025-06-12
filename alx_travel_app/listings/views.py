from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.exceptions import NotAuthenticated

# Create your views here.


class ListingViewSet(viewsets.ModelViewSet):
    """
    Listing viewset
    """
    serializer_class = ListingSerializer
    #permission_class = [IsAuthenticated, IsAdminUser]
    permission_class = [AllowAny]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated('You need to be authenticated')
        #return Listing.objects.filter(bookings__traveller=self.request.user)
        return Listing.objects.all()



class BookingViewSet(viewsets.ModelViewSet):
    """
    Booking viewset
    """
    serializer_class = BookingSerializer
    #permission_class = [IsAuthenticated, IsAdminUser]
    permission_class = [AllowAny]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated('You need to be authenticated')
        #return Booking.objects.filter(traveller=self.request.user)
        return Booking.objects.all()
