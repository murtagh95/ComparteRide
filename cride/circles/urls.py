""" Circles URLs. """

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import circles as circle_view
from .views import membership as membership_views

router = DefaultRouter()
router.register(r'circles', circle_view.CircleViewSet, basename='circle')
router.register(
    r'circles/(?P<slug_name>[-a-zA-Z0-9_]+)/members',
    membership_views.MembershipViewSet,
    basename='membership'
)

urlpatterns = [
    path('', include(router.urls)),
]
