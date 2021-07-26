""" Circles URLs. """

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import circles as circle_view

router = DefaultRouter()
router.register(r'circles', circle_view.CircleViewSet, basename='circle')

urlpatterns = [
    path('', include(router.urls)),
]
