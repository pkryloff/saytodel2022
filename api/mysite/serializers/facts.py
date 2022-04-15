from rest_framework import serializers

from api.mysite import LOGGER
from api.mysite.models.facts import MyFacts


class MyFactModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyFacts
        fields = [
            'id',
            'fact',
        ]

    def validate(self, data):
        fields_to_validate = [
            'owner',
            'fact',
        ]
        validated_data = {}
        for field in fields_to_validate:
            if field in data:
                # TODO: check type
                validated_data[field] = data[field]
            else:
                error = f'Facts {field} field is required'
                LOGGER.error(error)
                raise serializers.ValidationError(error)
        return validated_data

    def update(self, instance, validated_data):
        return serializers.ModelSerializer.update(self, instance, validated_data)

    def create(self, validated_data):
        return serializers.ModelSerializer.create(self, validated_data)
