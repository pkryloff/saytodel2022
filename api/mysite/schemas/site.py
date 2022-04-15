from drf_yasg import openapi

from api.mysite.serializers.site import MySiteModelSerializer


def get_serializer_response(http_code: int = 200, many: bool = False) -> dict:
    return {
        http_code: openapi.Response('MySite model response + Facts list', MySiteModelSerializer(many=many)),
    }


post_schema = openapi.Schema(
    title='MySite info schema',
    description='Schema to create MySite item',
    type=openapi.TYPE_OBJECT,
    properties={
        'description': openapi.Schema(type=openapi.TYPE_STRING,
                                      pattern='My name is Yoshikage Kira...', ),
        'color': openapi.Schema(type=openapi.TYPE_STRING,
                                pattern='Blue, LightBlue, Green, Purple, Red, Orange', ),
        'name': openapi.Schema(type=openapi.TYPE_STRING, pattern='Yoshikage Kira', ),
        'facts': openapi.Schema(type=openapi.TYPE_ARRAY,
                                items=openapi.Items(type=openapi.TYPE_STRING)),
    },
)

put_schema = openapi.Schema(
    title='MySite info schema',
    description='Schema to edit MySite item',
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, ),
        'description': openapi.Schema(type=openapi.TYPE_STRING,
                                      pattern='My name is Yoshikage Kira...', ),
        'color': openapi.Schema(type=openapi.TYPE_STRING,
                                pattern='Blue, LightBlue, Green, Purple, Red, Orange', ),
        'name': openapi.Schema(type=openapi.TYPE_STRING, pattern='Yoshikage Kira', ),
        'facts': openapi.Schema(type=openapi.TYPE_ARRAY,
                                items=openapi.Items(type=openapi.TYPE_STRING)),
    },
)

put_response = {
    **get_serializer_response(),
    400: 'MySite with {id} does not exist',
    403: 'Not the owner of MySite',
}

delete_schema = openapi.Schema(
    title='MySite info schema',
    description='Schema to delete MySite item',
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, ),
    },
)

delete_response = {
    **get_serializer_response(),
    400: 'MySite with {id} does not exist',
    403: 'Not the owner of MySite',
}
