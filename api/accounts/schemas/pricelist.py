from drf_yasg import openapi

from api.accounts.serializers.pricelist import PricelistModelSerializer


def get_serializer_response(http_code: int = 200, many: bool = False) -> dict:
    return {
        http_code: openapi.Response('Pricelist model response', PricelistModelSerializer(many=many)),
    }


post_schema = openapi.Schema(
    title='Pricelist info schema',
    description='Schema to create Pricelist item',
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, pattern='Пончик', ),
        'price': openapi.Schema(type=openapi.TYPE_STRING, pattern='42 BTC', ),
        'description': openapi.Schema(type=openapi.TYPE_STRING, pattern='Вкусный, сладкий, шоколадный', ),
    },
)

put_schema = openapi.Schema(
    title='Pricelist info schema',
    description='Schema to edit Pricelist item',
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, ),
        'name': openapi.Schema(type=openapi.TYPE_STRING, pattern='Пончик', ),
        'price': openapi.Schema(type=openapi.TYPE_STRING, pattern='42 BTC', ),
        'description': openapi.Schema(type=openapi.TYPE_STRING, pattern='Вкусный, сладкий, шоколадный', ),
    },
)

put_response = {
    **get_serializer_response(),
    400: 'Pricelist with {id} does not exist',
    403: 'Not the owner of Pricelist',
}

delete_schema = openapi.Schema(
    title='Pricelist info schema',
    description='Schema to delete Pricelist item',
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, ),
    },
)

delete_response = {
    **get_serializer_response(),
    400: 'Pricelist with {id} does not exist',
    403: 'Not the owner of Pricelist',
}
