from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mysite import LOGGER
from api.mysite.models.facts import MyFacts
from api.mysite.models.site import MySite
from api.mysite.schemas.facts import delete_response, delete_schema, get_serializer_response, \
    post_schema, put_response, put_schema
from api.mysite.serializers.facts import MyFactModelSerializer


class Facts(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(responses=get_serializer_response(many=True))
    def get(self, request):
        """
        Get user's MyFact items
        """
        items = MyFacts.objects.filter(owner=request.user)
        return Response(MyFactModelSerializer(items, many=True).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=post_schema, responses=get_serializer_response(http_code=201))
    def post(self, request):
        """
        Create new MyFact item
        """
        serializer = MyFactModelSerializer(request.user)
        data = request.data
        data['owner'] = request.user
        validated_data = serializer.validate(data)
        LOGGER.info('Request data validated')

        item = serializer.create(validated_data)
        LOGGER.info('New MyFact item added')

        return Response(MyFactModelSerializer(item).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=put_schema, responses=put_response)
    def put(self, request):
        """
        Edit MyFact item
        """
        item_id = None

        try:
            item_id = int(request.data['id'])
        except Exception as ex:
            error = f'An error occurred while getting MyFact id: {ex}'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        item = MyFacts.objects.filter(id=item_id).first()
        serializer = MyFactModelSerializer(request.user)

        if item is None:
            error = f'MyFact with {item_id} id does not exist'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        if request.user != item.owner:
            error = 'Not the owner of Fact'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        data['owner'] = request.user
        validated_data = serializer.validate(data)
        LOGGER.info('Request data validated')

        serializer.update(item, validated_data)
        LOGGER.info(f'MyFact {item.id} updated')

        return Response(MyFactModelSerializer(item).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=delete_schema, responses=delete_response)
    def delete(self, request):
        """
        Delete MyFact item
        """
        item_id = None

        try:
            item_id = int(request.data['id'])
        except Exception as ex:
            error = f'An error occurred while getting MyFact id: {ex}'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        item = MyFacts.objects.filter(id=item_id).first()

        if item is None:
            error = f'MyFact with {item_id} id does not exist'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        if request.user != item.owner:
            error = 'Not the owner of Fact'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_403_FORBIDDEN)

        item.delete()
        LOGGER.info(f'MyFact {item.id} deleted')

        return Response(MyFactModelSerializer(item).data, status=status.HTTP_200_OK)


class ViewFacts(APIView):
    @swagger_auto_schema(responses=get_serializer_response())
    def get(self, request, **kwargs):
        """
        Get user facts without token
        """
        name = self.kwargs.get('name')

        filter_res = MySite.objects.filter(name=name)
        if filter_res.count() == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        owner_id = filter_res.values().first()['owner_id']
        filter_res = MyFacts.objects.filter(owner=owner_id).values()

        return Response(filter_res, status=status.HTTP_200_OK)
