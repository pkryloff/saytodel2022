from drf_yasg import openapi

from api.accounts.serializers.gallery import GalleryModelSerializer


def get_serializer_response(http_code: int = 200, many: bool = False) -> dict:
    return {
        http_code: openapi.Response('Gallery model response', GalleryModelSerializer(many=many)),
    }


post_schema = openapi.Schema(
    title='Gallery info schema',
    description='Schema to create Gallery item',
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, pattern='Пончик', ),
        'description': openapi.Schema(type=openapi.TYPE_STRING,
                                      pattern='Вкусный, сладкий, шоколадный', ),
        'image_url': openapi.Schema(type=openapi.TYPE_STRING, pattern='https://clck.ru/UqdRT', ),
    },
)

put_schema = openapi.Schema(
    title='Gallery info schema',
    description='Schema to edit Gallery item',
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, ),
        'name': openapi.Schema(type=openapi.TYPE_STRING, pattern='Пончик', ),
        'description': openapi.Schema(type=openapi.TYPE_STRING,
                                      pattern='Вкусный, сладкий, шоколадный', ),
        'image_url': openapi.Schema(type=openapi.TYPE_STRING, pattern='https://clck.ru/UqdRT', ),
    },
)

put_response = {
    **get_serializer_response(),
    400: 'Gallery with {id} does not exist',
    403: 'Not the owner of Gallery'
}

delete_schema = openapi.Schema(
    title='Gallery info schema',
    description='Schema to delete Gallery item',
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, ),
    },
)

delete_response = {
    **get_serializer_response(),
    400: 'Gallery with {id} does not exist',
    403: 'Not the owner of Gallery'
}
