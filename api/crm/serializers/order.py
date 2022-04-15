from rest_framework import serializers

from api.crm import LOGGER
from api.crm.models.order import Order


class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'owner',
            'name',
            'contact',
            'status',
            'comment',
            'created_at',
            'updated_at',
        ]

    def validate(self, data):
        fields_to_validate = [
            'owner',
            'name',
            'contact',
            'status',
            'comment',
        ]
        validated_data = {}

        statuses = {'Новая', 'В работе', 'Выполнена', 'Отказ'}
        if 'status' in data:
            if data['status'] not in statuses:
                error = f'Status must be in {statuses}'
                LOGGER.error(error)
                raise serializers.ValidationError(error)

        for field in fields_to_validate:
            if field in data:
                validated_data[field] = data[field]

        return validated_data

    def update(self, instance, validated_data):
        return serializers.ModelSerializer.update(self, instance, validated_data)

    def create(self, validated_data):
        return serializers.ModelSerializer.create(self, validated_data)
