""" Circle model. """

# Django
from django.db import models

# Utilities
from cride.utils.models import CrideModel


class Circle(CrideModel):
    """ Circle model.

    A circle is a private group where rides are offered and taken by its
    members. To join a circle a user must receive an unique invitation
    code from an existing member. """
    name = models.CharField('circle name', max_length=140)
    slug_name = models.SlugField(unique=True, max_length=40)

    about = models.CharField('circle description', max_length=255)
    picture = models.ImageField(upload_to='circles/pictures',
                                blank=True,
                                null=True)
    members = models.ManyToManyField('users.User',
                                     through='circles.Membership',
                                     through_fields=('circle', 'user'))
    # Stats
    rides_offered = models.PositiveIntegerField(default=0)
    rides_taken = models.PositiveIntegerField(default=0)

    verified = models.BooleanField(
        'verified circle',
        default=False,
        help_text='Verified circle are also know as official communities.'
    )
    is_public = models.BooleanField(
        default=True,
        help_text='Public circles are listed in the main page so every'
                  'know about their existence.'
    )
    is_limited = models.BooleanField(
        'limited',
        default=True,
        help_text='Limited circles can grow up to a fixed number of member.'
    )
    members_limit = models.PositiveIntegerField(
        default=0,
        help_text='If circle is limited, this will be the limit on '
                  'the number of members.'
    )

    def __str__(self):
        """ Return circle name. """
        return self.name

    class Meta(CrideModel.Meta):
        """ Meta class. """
        ordering = ['-rides_taken', '-rides_offered']
