""" Circles admin. """

# Django
from django.contrib import admin

# Models
from cride.rides.models import Ride


@admin.register(Ride)
class CircleAdmin(admin.ModelAdmin):
    """ Circle admin. """
    list_display = ('offered_by', 'offered_in',
                    'available_seats', 'comments',
                    'departure_location', 'arrival_location')
    search_fields = ('offered_by', 'offered_in')
    list_filter = ('offered_by', 'offered_in',
                   'departure_date', 'arrival_date')
