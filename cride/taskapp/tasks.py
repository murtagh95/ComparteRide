""" Celery task. """

# Utilities
import jwt
from datetime import timedelta
import time

# Django
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

# Models
from cride.users.models import User
from cride.rides.models import Ride

# Celery
from cride.taskapp.celery import app
from celery.decorators import periodic_task


@app.task(name='send_confirmation_email', max_retries=3)
def send_confirmation_email(user_pk):
    """ Send account verification link to given user. """
    
    user = User.objects.get(pk=user_pk)
    verification_token = gen_verification_token(user)
    # Send Email
    subject = 'Welcome @{}! Verify your account to start using ' \
              'Comparte RIDE'.format(user.username)
    from_email = 'Comparte Ride <noreply@comparteride.com>'
    content = render_to_string(
        'emails/users/account_verification.html',
        {'token': verification_token, 'user': user}
    )
    msg = EmailMultiAlternatives(subject,
                                 content,
                                 from_email,
                                 [user.email])
    msg.attach_alternative(content, "text/html")
    msg.send()


def gen_verification_token(user):
    """ Create JWT token that the user can use to verify its account """
    exp_date = timezone.now() + timedelta(days=3)
    paylod = {
        'user': user.username,
        'exp': int(exp_date.timestamp()),
        'type': 'email_confirmation'
    }
    token = jwt.encode(
        paylod,
        settings.SECRET_KEY,
        algorithm='HS256'
    )
    return token.decode()


@periodic_task(name='disable_finished_rides', run_every=timedelta(minutes=20))
def disable_finished_rides():
    """ Disable finish rides. """
    now = timezone.now()
    offset = now + timedelta(minutes=20)
    
    # Update rides that have already finished
    rides = Ride.objects.filter(
        arrival_date__gte=now, 
        arrival_date__lte=offset,
        is_active=True
    )
    rides.update(is_active=False)
