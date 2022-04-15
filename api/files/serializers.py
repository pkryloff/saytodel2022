import base64
import io

from django.core.files.uploadedfile import UploadedFile
from rest_framework import serializers

from api.files import LOGGER
from api.files.models import Image
from api.utils import generate_filename


class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            'owner',
            'context',
            'created_at',
            'image',
        ]

    def validate(self, data):
        if 'image' not in data:
            error = 'No image data found'
            LOGGER.error(error)
            raise serializers.ValidationError(error)

        if 'ext' not in data['image']:
            error = 'No ext found'
            LOGGER.error(error)
            raise serializers.ValidationError(error)

        if data['image']['ext'] not in ('jpg', 'jpeg', 'png'):
            error = 'Incorrect image ext'
            LOGGER.error(error)
            raise serializers.ValidationError(error)

        if 'content' not in data['image']:
            error = 'No image content found'
            LOGGER.error(error)
            raise serializers.ValidationError(error)

        image_data = data['image']

        try:
            image_content = image_data['content'].split('base64,')[-1]
            image_bytes = base64.b64decode(image_content)
            stream = io.BytesIO(image_bytes)
            data['image'] = UploadedFile(stream, name=generate_filename(image_data['ext']))
        except Exception as ex:
            error = f'An error occurred while processing the uploaded image: {ex}'
            LOGGER.error(error)
            raise serializers.ValidationError(error)

        return data

    def create(self, validated_data):
        return serializers.ModelSerializer.create(self, validated_data)
