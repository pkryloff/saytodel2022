from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mysite import LOGGER
from api.mysite.models.facts import MyFacts
from api.mysite.models.site import MySite
from api.mysite.schemas.site import delete_response, delete_schema, get_serializer_response, \
    post_schema, put_response, put_schema
from api.mysite.serializers.facts import MyFactModelSerializer
from api.mysite.serializers.site import MySiteModelSerializer


class Site(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(responses=get_serializer_response(many=True))
    def get(self, request):
        """
        Get user's MySite items
        """
        items = MySite.objects.filter(owner=request.user)
        facts = MyFacts.objects.filter(owner=request.user)

        facts_list = []
        for fact in facts.values():
            facts_list.append(fact['fact'])

        site_data = MySiteModelSerializer(items, many=True).data
        for item in site_data:
            item['facts'] = facts_list

        return Response(site_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=post_schema, responses=get_serializer_response(http_code=201))
    def post(self, request):
        """
        Create new MySite item
        """
        items = MySite.objects.filter(owner=request.user)
        if items.count() > 0:
            return Response('MySite for this user already exists',
                            status=status.HTTP_400_BAD_REQUEST)

        if MySite.objects.filter(name=request.data['name']):
            return Response('MySite with this name already exists',
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = MySiteModelSerializer(request.user)
        data = request.data

        facts_list = data.get('facts', [])
        for fact in facts_list:
            fact_serializer = MyFactModelSerializer(request.user)
            fact_data = {'fact': fact, 'owner': request.user}
            validated_fact_data = fact_serializer.validate(fact_data)
            fact_serializer.create(validated_fact_data)
            LOGGER.info('New MyFact item added')

        data['owner'] = request.user
        validated_data = serializer.validate(data)
        LOGGER.info('Request data validated')

        item = serializer.create(validated_data)
        LOGGER.info('New MySite item added')

        site_data = MySiteModelSerializer(item).data
        site_data['facts'] = facts_list

        return Response(site_data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=put_schema, responses=put_response)
    def put(self, request):
        """
        Edit MySite item
        """
        item_id = None

        try:
            item_id = int(request.data['id'])
        except Exception as ex:
            error = f'An error occurred while getting MySite id: {ex}'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        item = MySite.objects.filter(id=item_id).first()
        serializer = MySiteModelSerializer(request.user)

        if item is None:
            error = f'MySite with {item_id} id does not exist'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        if request.user != item.owner:
            error = 'Not the owner of MySite'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_403_FORBIDDEN)

        data = request.data

        MyFacts.objects.filter(owner=request.user).delete()

        facts_list = data.get('facts', [])
        for fact in facts_list:
            fact_serializer = MyFactModelSerializer(request.user)
            fact_data = {'fact': fact, 'owner': request.user}
            validated_fact_data = fact_serializer.validate(fact_data)
            fact_serializer.create(validated_fact_data)
            LOGGER.info('New MyFact item added')

        data['owner'] = request.user
        validated_data = serializer.validate(data)
        LOGGER.info('Request data validated')

        serializer.update(item, validated_data)
        LOGGER.info(f'MySite {item.id} updated')

        site_data = MySiteModelSerializer(item).data
        site_data['facts'] = facts_list

        return Response(site_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=delete_schema, responses=delete_response)
    def delete(self, request):
        """
        Delete MySite item
        """
        item_id = None

        try:
            item_id = int(request.data['id'])
        except Exception as ex:
            error = f'An error occurred while getting MySite id: {ex}'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        item = MySite.objects.filter(id=item_id).first()

        if item is None:
            error = f'MySite with {item_id} id does not exist'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        if request.user != item.owner:
            error = 'Not the owner of MySite'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_403_FORBIDDEN)

        facts = MyFacts.objects.filter(owner=request.user)
        facts_list = []
        for fact in facts.values():
            facts_list.append(fact['fact'])

        facts.delete()
        LOGGER.info(f'Facts of MySite {item.id} deleted')

        item.delete()
        LOGGER.info(f'MySite {item.id} deleted')

        site_data = MySiteModelSerializer(item).data
        site_data['facts'] = facts_list

        return Response(site_data, status=status.HTTP_200_OK)


class ViewSite(APIView):
    name_kwarg = 'name'

    @swagger_auto_schema(responses=get_serializer_response(many=True))
    def get(self, request, **kwargs):
        """
        Get MySite item from name
        """
        name = self.kwargs.get('name')

        filter_res = MySite.objects.filter(name=name)
        if filter_res.count() == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        item = filter_res.values().first()
        facts = MyFacts.objects.filter(owner=filter_res.first().owner)

        fact_list = []
        for fact in facts.values():
            fact_list.append(fact['fact'])

        item['facts'] = fact_list
        return Response(item, status=status.HTTP_200_OK)
