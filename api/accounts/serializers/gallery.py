from rest_framework import serializers

from api.accounts.models.gallery import Gallery


class GalleryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = [
            'id',
            'owner',
            'name',
            'description',
            'image_url',
        ]

    def validate(self, data):
        fields_to_validate = [
            'owner',
            'name',
            'description',
            'image_url',
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
