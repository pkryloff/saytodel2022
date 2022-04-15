from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.files import LOGGER
from api.files.models import Image
from api.files.schemas import delete_response, delete_schema, upload_response, upload_schema
from api.files.serializers import ImageModelSerializer
from Samodelkin.settings import MEDIA_URL


class Upload(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=upload_schema, responses=upload_response)
    def post(self, request):
        """
        Upload an image
        """
        serializer = ImageModelSerializer()

        data = request.data
        data['owner'] = request.user
        validated_data = serializer.validate(data)
        LOGGER.info('Request data validated')

        uploaded_object = serializer.create(validated_data)
        LOGGER.info('Image uploaded')

        return Response(ImageModelSerializer(uploaded_object).data['image'],
                        status=status.HTTP_201_CREATED)


class Delete(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=delete_schema, responses=delete_response)
    def delete(self, request):
        """
        Delete an uploaded image
        """
        image_url: str

        try:
            image_url = request.data['image_url']
        except Exception as ex:
            error = f'An error occurred while getting image_url: {ex}'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        image_path = image_url.partition(MEDIA_URL)[-1]
        item = Image.objects.filter(image=image_path).first()

        if item is None:
            error = f'Image with {image_url} url does not exist'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        if item.owner != request.user:
            error = 'Not the owner of image'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_403_FORBIDDEN)

        item.delete()
        LOGGER.info(f'Image {item.image} (id={item.id}) deleted')

        return Response('Image deleted', status=status.HTTP_200_OK)
