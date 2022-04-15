from drf_yasg import openapi

from api.crm.serializers.order import OrderModelSerializer


def get_serializer_response(http_code: int = 200, many: bool = False) -> dict:
    return {
        http_code: openapi.Response('Order model response', OrderModelSerializer(many=many)),
    }


get_schema = [
    openapi.Parameter(name='offset', in_=openapi.IN_QUERY,
                      required=False, type=openapi.TYPE_INTEGER, ),
    openapi.Parameter(name='limit', in_=openapi.IN_QUERY,
                      required=False, type=openapi.TYPE_INTEGER, )
]

post_schema = openapi.Schema(
    description='Schema to create Order',
    type=openapi.TYPE_OBJECT,
    properties={
        'site': openapi.Schema(type=openapi.TYPE_STRING, pattern='somesitename', ),
        'name': openapi.Schema(type=openapi.TYPE_STRING, pattern='Сергей Кузьмич', ),
        'contact': openapi.Schema(type=openapi.TYPE_STRING, pattern='+7 (123) 456-78-90', ),
        'status': openapi.Schema(type=openapi.TYPE_STRING, pattern='В работе', ),
        'comment': openapi.Schema(type=openapi.TYPE_STRING, pattern='Требуется ремонт раковины', ),
    },
)

put_schema = openapi.Schema(
    description='Schema to edit Order',
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, ),
        'name': openapi.Schema(type=openapi.TYPE_STRING, pattern='Сергей Кузьмич', ),
        'contact': openapi.Schema(type=openapi.TYPE_STRING, pattern='+7 (123) 456-78-90', ),
        'status': openapi.Schema(type=openapi.TYPE_STRING, pattern='В работе', ),
        'comment': openapi.Schema(type=openapi.TYPE_STRING, pattern='Требуется ремонт раковины', ),
    },
)

put_response = {
    **get_serializer_response(),
    400: 'Order with {id} does not exist',
    403: 'Not the owner of Order',
}

delete_schema = openapi.Schema(
    description='Schema to delete Order',
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, ),
    },
)

delete_response = {
    **get_serializer_response(),
    400: 'Order with {id} does not exist',
    403: 'Not the owner of Order',
}
