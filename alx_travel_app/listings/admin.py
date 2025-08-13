from django.contrib import admin
from .models import User, Listing, Booking, Review

# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Booking)
admin.site.register(Review)