""" Circles serializers. """

# Django REST Framework
from rest_framework import serializers

# Models
from cride.circles.models import Circle


class CircleModelSerializer(serializers.ModelSerializer):
    """ Circle model serializer. """
    members_limit = serializers.IntegerField(
        required=False,
        min_value=10,
        max_value=32000
    )
    is_limited = serializers.BooleanField(default=False)

    class Meta:
        """ Meta class. """
        model = Circle
        fields = (
            'id', 'name',
            'slug_name', 'about',
            'picture', 'rides_offered',
            'rides_taken', 'verified',
            'is_public', 'is_limited',
            'members_limit'
        )
        read_only_fields = (
            'is_public',
            'verified',
            'rides_taken',
            'rides_offered'
        )

    def validate(self, attrs):
        """ Ensure both members_list and is_limited are present. """
        members_limit = attrs.get('members_limit', None)
        is_limited = attrs.get('is_limited', False)
        if is_limited ^ bool(members_limit):
            raise serializers.ValidationError(
                'If circle is limited, a member limit must be provided')
        return attrs
