from django.urls import path, include
from . import views
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter


router = DefaultRouter()
router.register('bookings', views.BookingViewSet, basename='booking')
router.register('listings', views.ListingViewSet, basename='listing')




urlpatterns = [
    path('', include(router.urls)),
]
