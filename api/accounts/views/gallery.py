from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.accounts import LOGGER
from api.accounts.models import gallery
from api.accounts.schemas.gallery import delete_response, delete_schema, get_serializer_response, \
    post_schema, put_response, put_schema
from api.accounts.serializers.gallery import GalleryModelSerializer


class Gallery(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(responses=get_serializer_response(many=True))
    def get(self, request):
        """
        Get user's Gallery items
        """
        items = gallery.Gallery.objects.filter(owner=request.user)
        return Response(GalleryModelSerializer(items, many=True).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=post_schema, responses=get_serializer_response(http_code=201))
    def post(self, request):
        """
        Create new Gallery item
        """
        serializer = GalleryModelSerializer(request.user)

        data = request.data
        data['owner'] = request.user
        validated_data = serializer.validate(data)
        LOGGER.info('Request data validated')

        item = serializer.create(validated_data)
        LOGGER.info('New gallery item added')

        return Response(GalleryModelSerializer(item).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=put_schema, responses=put_response)
    def put(self, request):
        """
        Edit Gallery item
        """
        item_id: int

        try:
            item_id = int(request.data['id'])
        except Exception as ex:
            error = f'An error occurred while getting gallery id: {ex}'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        item = gallery.Gallery.objects.filter(id=item_id).first()
        serializer = GalleryModelSerializer(request.user)

        if item is None:
            error = f'Gallery with {item_id} id does not exist'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        if request.user != item.owner:
            error = 'Not the owner of Gallery'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        data['owner'] = request.user
        validated_data = serializer.validate(data)
        LOGGER.info('Request data validated')

        serializer.update(item, validated_data)
        LOGGER.info(f'Gallery {item.id} updated')

        return Response(GalleryModelSerializer(item).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=delete_schema, responses=delete_response)
    def delete(self, request):
        """
        Delete Gallery item
        """
        item_id: int

        try:
            item_id = int(request.data['id'])
        except Exception as ex:
            error = f'An error occurred while getting gallery id: {ex}'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        item = gallery.Gallery.objects.filter(id=item_id).first()

        if item is None:
            error = f'Gallery with {item_id} id does not exist'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        if request.user != item.owner:
            error = 'Not the owner of Gallery'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_403_FORBIDDEN)

        item.delete()
        LOGGER.info(f'Gallery {item.id} deleted')

        return Response(GalleryModelSerializer(item).data, status=status.HTTP_200_OK)


class ViewGallery(APIView):
    @swagger_auto_schema(responses=get_serializer_response(many=True))
    def get(self, request, **kwargs):
        """
        Get user's Gallery items without token
        """
        user_id = self.kwargs.get('user_id')

        try:
            user_id = int(user_id)
        except Exception as ex:
            error = f'Exception in ViewGallery: {ex}'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        filter_res = gallery.Gallery.objects.filter(owner=user_id)
        return Response(GalleryModelSerializer(filter_res, many=True).data,
                        status=status.HTTP_200_OK)
