""" Users serializers. """

# Django
from django.contrib.auth import authenticate

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token

# Models
from cride.users.models import User


class UserModelSerializer(serializers.ModelSerializer):
    """ User model serializer. """
    class Meta:
        """ Meta class. """
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'phone_number'
        )


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
        self.context['user'] = user
        return attrs

    def create(self, validated_data):
        """Generate or retrieve new token"""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key
