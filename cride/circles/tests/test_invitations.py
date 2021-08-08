""" Invitations tests. """

# Django
from django.test import TestCase

# Django REST Framework
from rest_framework.test import APITestCase
from rest_framework import status

# Models
from cride.circles.models import Invitation, Circle, Membership
from cride.users.models import User, Profile
from rest_framework.authtoken.models import Token

# Manager
from cride.circles.managers import InvitationManager


class InvitationsManagerTestCase(TestCase):
    """ Invitations manager test case. """

    def setUp(self):
        """ Test case setup. """
        self.user = User.objects.create(
            first_name='Nicolas',
            last_name='Catalano',
            email='nec.catalano@gmail.com',
            username='nicolasCatalano',
            password='nico1234'
        )

        self.circle = Circle.objects.create(
            name='Facultad de Ciencias',
            slug_name='fciencias',
            about='Grupo oficial de la Facultad de Ciencias de la UNAM',
            verified=True
        )
        
    def test_code_generation(self):
        """ Random codes should e generated automatically. """
        invitation = Invitation.objects.create(
            issue_by=self.user,
            circle=self.circle
        )
        code_length = InvitationManager().CODE_LENGTH
        
        self.assertIsNotNone(invitation.code)
        self.assertEqual(len(invitation.code), code_length)
        self.assertIsInstance(invitation.code, str)
    
    def test_code_usage(self):
        """ If a code is given, there's no nedd to create a new one. """
        code = 'holaMundo'
        invitation = Invitation.objects.create(
            issue_by=self.user,
            circle=self.circle,
            code=code
        )
        self.assertEqual(invitation.code, code)

    def test_code_generation_if_duplicated(self):
        """ If given code is not unique, a new one must be generated. """
        code = Invitation.objects.create(
            issue_by=self.user,
            circle=self.circle,
        ).code

        # Create another invitation with the past code
        invitation = Invitation.objects.create(
            issue_by=self.user,
            circle=self.circle,
            code=code
        )
        self.assertNotEqual(invitation.code, code)


class MemberInvitationsAPITestCase(APITestCase):
    """ Member invitation API test case. """

    def setUp(self):
        """ Test case setup. """
        self.user = User.objects.create(
            first_name='Nicolas',
            last_name='Catalano',
            email='nec.catalano@gmail.com',
            username='nicolasCatalano',
            password='nico1234'
        )

        self.profile = Profile.objects.create(
            user=self.user
        )

        self.circle = Circle.objects.create(
            name='Facultad de Ciencias',
            slug_name='fciencias',
            about='Grupo oficial de la Facultad de Ciencias de la UNAM',
            verified=True
        )
        
        self.membership = Membership.objects.create(
            user=self.user,
            profile=self.profile,
            circle=self.circle,
            remaining_invitations=10
        )
        # Auth
        self.token = Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        
        # URL
        self.url = '/circles/{}/members/{}/invitations/'.format(
            self.circle.slug_name,
            self.user.username
        )
    
    def test_success(self):
        """ Verify request success. """
        
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_invitation_creation(self):
        """ Verify invitation are generated if none exist previosly.  """
        # Invitations in DB must be 0
        self.assertEqual(Invitation.objects.count(), 0)
        
        # Call member invitations URL
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

        # Verify new invitations were created
        invitations = Invitation.objects.filter(issue_by=self.user)
        self.assertEqual(invitations.count(), self.membership.remaining_invitations)
        for inv in invitations:
            self.assertIn(inv.code, request.data['invitations'])
