from drf_yasg import openapi

from api.accounts.serializers.profile import UserModelSerializer


def get_serializer_response(http_code: int = 200, many: bool = False) -> dict:
    return {
        http_code: openapi.Response('User model response', UserModelSerializer(many=many)),
    }


post_schema = openapi.Schema(
    title='User profile info schema',
    description='Schema to set or update user profile info',
    type=openapi.TYPE_OBJECT,
    properties={
        'image_url': openapi.Schema(type=openapi.TYPE_STRING,
                                    pattern='https://amazon/media/folder/date/filename.jpg', ),
        'first_name': openapi.Schema(type=openapi.TYPE_STRING, pattern='Сергей', ),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING, pattern='Кузьмич', ),
        'gender': openapi.Schema(type=openapi.TYPE_STRING, pattern='Мужской', ),
        'phone': openapi.Schema(type=openapi.TYPE_STRING, pattern='+71234567890', ),
        'address': openapi.Schema(type=openapi.TYPE_STRING, pattern='Кострома, ул. Ленина, д. 5', ),
        'occupation': openapi.Schema(type=openapi.TYPE_STRING, pattern='Кондитер', ),
        'inn': openapi.Schema(type=openapi.TYPE_STRING, pattern='000000000000', ),
        'vk': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                             pattern='https://vk.com/some_username', ),
        'instagram': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                    pattern='https://www.instagram.com/some_username/', ),
        'facebook': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                   pattern='https://www.facebook.com/some_username/', ),
        'website': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                  pattern='https://ppnp.me', ),
    },
)
