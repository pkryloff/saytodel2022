from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.accounts.models.profile import User
from api.crm import LOGGER
from api.crm.models import order
from api.crm.schemas.order import delete_response, delete_schema, get_schema, \
    get_serializer_response, post_schema, put_response, put_schema
from api.crm.serializers.order import OrderModelSerializer
from api.mysite.models.site import MySite
from Samodelkin.settings import DEFAULT_FROM_EMAIL


class UnauthenticatedPost(BasePermission):
    def has_permission(self, request, view):
        return request.method in ['POST']


class Order(APIView):
    permission_classes = [IsAuthenticated | UnauthenticatedPost]

    @swagger_auto_schema(manual_parameters=get_schema,
                         responses=get_serializer_response(many=True))  # TODO: add `total` to schema
    def get(self, request):
        """
        Get user's orders
        """
        offset = int(request.query_params.get('offset', 0))
        limit = int(request.query_params.get('limit', 10))
        items = order.Order.objects.filter(owner=request.user).order_by('-updated_at')
        return Response({'total': len(items),
                         'orders': OrderModelSerializer(items[offset:offset + limit], many=True).data},
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=post_schema, responses=get_serializer_response(http_code=201))
    def post(self, request):
        """
        Create new Order item
        """
        serializer = OrderModelSerializer(request.user)
        data = request.data

        send_notification = False

        if 'site' in data:
            # define owner of the order
            site_filter = MySite.objects.filter(name=data['site'])
            if site_filter.count() == 0:
                return Response(status=status.HTTP_404_NOT_FOUND)
            site_item = site_filter.first()
            data['owner'] = site_item.owner
            send_notification = True
        else:
            data['owner'] = request.user

        validated_data = serializer.validate(data)
        LOGGER.info('Request data validated')

        item = serializer.create(validated_data)
        LOGGER.info('New Order item added')

        # send email notification
        if send_notification:
            owner = User.objects.filter(id=data['owner'].id).first()
            subject = 'Новая заявка'
            html_msg = render_to_string('crm/new_order.html', {'username': owner.first_name,
                                                               'client_name': validated_data.get('name', 'отсутствует'),
                                                               'contact': validated_data.get('contact', 'отсутствует'),
                                                               'comment': validated_data.get('comment', 'отсутствует')
                                                               })
            plain_msg = strip_tags(html_msg)
            mail.send_mail(subject=subject, message=plain_msg,
                           from_email=DEFAULT_FROM_EMAIL, recipient_list=[owner.email],
                           html_message=html_msg, fail_silently=True)

        return Response(OrderModelSerializer(item).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=put_schema, responses=put_response)
    def put(self, request):
        """
        Edit Order item
        """
        item_id: int

        try:
            item_id = int(request.data['id'])
        except Exception as ex:
            error = f'An error occurred while getting order id: {ex}'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        item = order.Order.objects.filter(id=item_id).first()
        serializer = OrderModelSerializer(request.user)

        if item is None:
            error = f'Order with {item_id} id does not exist'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        if request.user != item.owner:
            error = 'Not the owner of Order'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        data['owner'] = request.user
        validated_data = serializer.validate(data)
        LOGGER.info('Request data validated')

        serializer.update(item, validated_data)
        LOGGER.info(f'Order {item.id} updated')

        return Response(OrderModelSerializer(item).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=delete_schema, responses=delete_response)
    def delete(self, request):
        """
        Delete Order item
        """
        item_id: int

        try:
            item_id = int(request.data['id'])
        except Exception as ex:
            error = f'An error occurred while getting order id: {ex}'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        item = order.Order.objects.filter(id=item_id).first()

        if item is None:
            error = f'Order with {item_id} id does not exist'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        if request.user != item.owner:
            error = 'Not the owner of Order'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_403_FORBIDDEN)

        item.delete()
        LOGGER.info(f'Order {item.id} deleted')

        return Response(OrderModelSerializer(item).data, status=status.HTTP_200_OK)


class OrderStatus(APIView):
    permission_classes = [IsAuthenticated | UnauthenticatedPost]

    def get(self, request):
        """
        Get user orders' status
        """
        new = order.Order.objects.filter(owner=request.user).filter(status='Новая').count()
        in_progress = order.Order.objects.filter(owner=request.user).filter(status='В работе').count()
        return Response({'new': new, 'in_progress': in_progress}, status=status.HTTP_200_OK)
