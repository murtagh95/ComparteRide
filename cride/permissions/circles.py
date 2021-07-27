""" Circles permission class. """

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from cride.circles.models import Memberships


class IsCircleAdmin(BasePermission):
    """ Allow access only to circle admins. """
    def has_object_permission(self, request, view, obj):
        """ Verify user have a membership in the obj. """
        try:
            Memberships.objects.get(
                user=request.user,
                circle=obj,
                is_admin=True,
                is_active=True
            )
        except Memberships.DoesNotExist:
            return False
        return True
