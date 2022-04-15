from drf_yasg import openapi

from api.files.serializers import ImageModelSerializer


def get_serializer_response(http_code: int = 200, many: bool = False) -> dict:
    return {
        http_code: openapi.Response('Image model response', ImageModelSerializer(many=many)),
    }


upload_schema = openapi.Schema(
    title='Image upload schema',
    description='Schema to upload an image to user profile',
    type=openapi.TYPE_OBJECT,
    required=['image'],
    properties={
        'context': openapi.Schema(type=openapi.TYPE_STRING, pattern='profile/gallery', ),
        'image': openapi.Schema(type=openapi.TYPE_OBJECT,
                                required=['ext', 'content'],
                                properties={
                                    'ext': openapi.Schema(type=openapi.TYPE_STRING,
                                                          pattern='jpg', ),
                                    'content': openapi.Schema(type=openapi.TYPE_STRING,
                                                              format=openapi.FORMAT_BASE64,
                                                              ),
                                },
                                ),
    },
)

upload_response = {
    201: openapi.Schema(title='image_url', type=openapi.TYPE_STRING, ),
}

delete_schema = openapi.Schema(
    title='Image delete schema',
    description='Schema to delete an uploaded image',
    type=openapi.TYPE_OBJECT,
    required=['image_url'],
    properties={
        'image_url': openapi.Schema(type=openapi.TYPE_STRING, ),
    },
)

delete_response = {
    200: 'Image deleted',
    400: 'Image with {url} does not exist',
    403: 'Not the owner of image',
}
