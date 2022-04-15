from drf_yasg import openapi

from api.mysite.serializers.facts import MyFactModelSerializer


def get_serializer_response(http_code: int = 200, many: bool = False) -> dict:
    return {
        http_code: openapi.Response('MyFact model response', MyFactModelSerializer(many=many)),
    }


post_schema = openapi.Schema(
    title='MyFact info schema',
    description='Schema to create MyFact item',
    type=openapi.TYPE_OBJECT,
    properties={
        'fact': openapi.Schema(type=openapi.TYPE_STRING, pattern='2+2=4', ),
    },
)

put_schema = openapi.Schema(
    title='MyFact info schema',
    description='Schema to edit MyFacts item',
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, ),
        'fact': openapi.Schema(type=openapi.TYPE_STRING, pattern='2+2=4', ),
    },
)

put_response = {
    **get_serializer_response(),
    400: ' yFact with {id} does not exist',
    403: 'Not the owner of MyFact',
}

delete_schema = openapi.Schema(
    title='MyFact info schema',
    description='Schema to delete MyFact item',
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, ),
    },
)

delete_response = {
    **get_serializer_response(),
    400: 'MyFact with {id} does not exist',
    403: 'Not the owner of MyFact',
}
