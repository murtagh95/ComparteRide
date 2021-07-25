""" Circles URLs. """

# Django
from django.urls import path

# Views
from cride.circles.views import list_circles, create_circle


urlpatterns = [
    path('circles/', list_circles, name='circle'),
    path('circles/create', create_circle, name='create circle'),
]
