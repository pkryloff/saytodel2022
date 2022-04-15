from drf_yasg import openapi

get_schema = [
    openapi.Parameter(name='offset', in_=openapi.IN_QUERY,
                      required=False, type=openapi.TYPE_INTEGER, ),
    openapi.Parameter(name='limit', in_=openapi.IN_QUERY,
                      required=False, type=openapi.TYPE_INTEGER, ),
    openapi.Parameter(name='search_term', in_=openapi.IN_QUERY,
                      required=False, type=openapi.TYPE_STRING, ),
    openapi.Parameter(name='min_rank', in_=openapi.IN_QUERY,
                      required=False, type=openapi.TYPE_NUMBER, )

]

get_response = {
    200: openapi.Schema(
        description='Card info',
        type=openapi.TYPE_ARRAY,
        items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, pattern='Сергей', ),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, pattern='Кузьмич', ),
                'occupation': openapi.Schema(type=openapi.TYPE_STRING, pattern='Кондитер', ),
                'image_url': openapi.Schema(type=openapi.TYPE_STRING,
                                            pattern='https://amazon/media/folder/date/filename.jpg', ),
                'address': openapi.Schema(type=openapi.TYPE_STRING, pattern='Кострома, ул. Ленина, д. 5', ),
                'verified': openapi.Schema(type=openapi.TYPE_BOOLEAN, ),
                'site_name': openapi.Schema(type=openapi.TYPE_STRING, pattern='somesitename', ),
            }
        )
    )
}
