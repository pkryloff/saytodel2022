from rest_framework import serializers

from api.accounts.models.pricelist import Pricelist


class PricelistModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricelist
        fields = [
            'id',
            'owner',
            'name',
            'price',
            'description',
        ]

    def validate(self, data):
        fields_to_validate = [
            'owner',
            'name',
            'price',
            'description',
        ]
        validated_data = {}
        for field in fields_to_validate:
            if field in data:
                validated_data[field] = data[field]
        return validated_data

    def update(self, instance, validated_data):
        return serializers.ModelSerializer.update(self, instance, validated_data)

    def create(self, validated_data):
        return serializers.ModelSerializer.create(self, validated_data)
