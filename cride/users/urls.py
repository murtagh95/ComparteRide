""" Users URLs. """

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from cride.users.views import users as user_views

router = DefaultRouter()
router.register(r'users', user_views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
