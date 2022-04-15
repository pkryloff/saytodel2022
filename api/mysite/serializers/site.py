import re

from rest_framework import serializers

from api.mysite import LOGGER
from api.mysite.models.site import MySite

CHARS_DIGITS_UNDERSCORE = re.compile(r'^[\w()-]+$', re.ASCII)
MINIMUM_NAME_LENGTH = 4
STOP_LIST = [s.lower() for s in [
    # Reserved keywords
    'api',
    'login',
    'logout',
    'me',
    'my-cards',
    'marketplace',
    'my-requests',
    'my-site',
    'about-us',
    'registration',
    'policy',
    'verify-user',

    # Blacklist
    '',
    'admin',
    'administator',
    'moderator',
    'samodelkin',
]]
COLORS = {'Blue', 'LightBlue', 'Green', 'Purple', 'Red', 'Orange'}


class MySiteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MySite
        fields = [
            'id',
            'description',
            'color',
            'name',
            'created_at',
            'updated_at',
        ]

    def validate(self, data):
        fields_to_validate = [
            'owner',
            'description',
            'color',
            'name',
        ]
        validated_data = {}

        if 'color' in data:
            if data['color'] not in COLORS:
                error = f'Color must be in {COLORS}'
                LOGGER.error(error)
                raise serializers.ValidationError(error)

        if 'name' in data:
            name_check = str(data['name'])
            if not CHARS_DIGITS_UNDERSCORE.match(name_check):
                error = 'Name contains prohibited symbols'
                LOGGER.error(error)
                raise serializers.ValidationError(error)
            if name_check.lower() in STOP_LIST:
                error = 'Name is in stop-list'
                LOGGER.error(error)
                raise serializers.ValidationError(error)
            if len(name_check) < MINIMUM_NAME_LENGTH:
                error = f'Name is shorter than {MINIMUM_NAME_LENGTH} symbols'
                LOGGER.error(error)
                raise serializers.ValidationError(error)

        for field in fields_to_validate:
            if field in data and field != 'facts':
                # TODO: check type, name is correct
                validated_data[field] = data[field]
            else:
                error = f'MySite {field} field is required'
                LOGGER.error(error)
                raise serializers.ValidationError(error)
        return validated_data

    def update(self, instance, validated_data):
        return serializers.ModelSerializer.update(self, instance, validated_data)

    def create(self, validated_data):
        return serializers.ModelSerializer.create(self, validated_data)
