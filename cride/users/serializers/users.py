""" Users serializers. """

# Utilities
import jwt

# Taskas
from cride.taskapp.tasks import send_confirmation_email

# Django
from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator
from django.conf import settings

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

# Models
from cride.users.models import User, Profile

# Serializer
from cride.users.serializers.profile import ProfileModelSerializer


class UserModelSerializer(serializers.ModelSerializer):
    """ User model serializer. """

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        """ Meta class. """
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'profile'
        )


class UserSignUpSerializer(serializers.Serializer):
    """ User sign up serializer.

    Hadle sign up data validation and user/profile creation.
    """
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    # Phone number
    phone_regex = RegexValidator(
        regex='\+?1?\d{9,15}$',
        message='Phone number must be entered in the format: +123456789. Up '
                'to 15 digits allowed.'
    )
    phone_number = serializers.CharField(validators=[phone_regex])
    # Password
    password = serializers.CharField(min_length=8,
                                     max_length=64)
    password_confirmation = serializers.CharField(min_length=8,
                                                  max_length=64)
    # Name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self, attrs: dict):
        """ Verify passwords match. """
        password = attrs['password']
        password_conf = attrs['password_confirmation']
        if password != password_conf:
            raise serializers.ValidationError(
                "Passwords don't match."
            )
        password_validation.validate_password(password)
        return attrs

    def create(self, validated_data):
        """ Handle user and profile creation. """
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(**validated_data,
                                        is_verified=False,
                                        is_client=True)
        Profile.objects.create(user=user)
        send_confirmation_email.delay(user_pk=user.pk)
        return user


class UserLoginSerializer(serializers.Serializer):
    """ User login serializer.
    Handle the login request data. """
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8,
                                     max_length=64)

    def validate(self, attrs: dict):
        """ Check credentials. """
        user = authenticate(username=attrs['email'],
                            password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet.')
        self.context['user'] = user
        return attrs

    def create(self, validated_data):
        """Generate or retrieve new token"""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class AccountVerificationSerializer(serializers.Serializer):
    """ Account verification serializer. """
    token = serializers.CharField()

    def validate_token(self, data):
        """ Verify token is valid. """
        try:
            payload = jwt.decode(data,
                                 settings.SECRET_KEY,
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token.')

        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token.')

        self.context['payload'] = payload
        return data

    def save(self, **kwargs):
        """ Update user's verified status. """
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()
