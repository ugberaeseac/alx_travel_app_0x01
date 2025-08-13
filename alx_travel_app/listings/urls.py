
from django.urls import path, include
from rest_framework import routers
from listings.views import UserViewSet, ListingViewSet, BookingViewSet, ReviewViewSet



router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user-view')
router.register(r'listings', ListingViewSet, basename='listing-view')
router.register(r'bookings', BookingViewSet, basename='booking-view')
router.register(r'reviews', ReviewViewSet, basename='review-view')




urlpatterns = [
    path('', include((router.urls, 'listings'))),

]

#urlpatterns += router.urls
