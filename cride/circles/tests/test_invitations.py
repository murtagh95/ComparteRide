""" Invitations tests. """

# Django
from django.test import TestCase

# Models
from cride.circles.models import Invitation, Circle
from cride.users.models import User

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
