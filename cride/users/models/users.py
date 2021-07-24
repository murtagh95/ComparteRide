""" User model. """

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Utilities
from cride.utils.models import CrideModel


class User(CrideModel, AbstractUser):
    """ User model.

    Extend from Dkango's Abstract User, change the username fields
    to email and add some extra fields.
    """
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )
    phone_regex = RegexValidator(
        regex='\+?1?\d{9,15}$',
        message='Phone number must be entered in the format: +123456789. Up '
                'to 15 digits allowed.'
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True
    )
    is_client = models.BooleanField(
        'client',
        default=True,
        help_text=(
            'Help easily distinguish users and perform queries.'
            'Clients are the main type of user.'
        )
    )
    is_verfied = models.BooleanField(
        'verified',
        default=False,
        help_text='Set to true when the user have verified its email address.'
    )

    USERNAME_FIELD = 'email'  # Change the username fields
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self) -> str:
        """Return username. """
        return self.username

    def get_short_name(self) -> str:
        """ Return username. """
        return self.username
