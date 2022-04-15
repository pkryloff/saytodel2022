from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.accounts import LOGGER
from api.accounts.models.profile import User
from api.accounts.schemas.profile import get_serializer_response, post_schema
from api.accounts.serializers.profile import UserModelSerializer


class Profile(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(responses=get_serializer_response())
    def get(self, request):
        """
        Get user profile info
        """
        serializer = UserModelSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=post_schema, responses=get_serializer_response())
    def post(self, request):
        """
        Set or update user profile info
        """
        serializer = UserModelSerializer(request.user)

        validated_data = serializer.validate(request.data)
        LOGGER.info('Request data validated')

        serializer.update(request.user, validated_data)
        LOGGER.info('User data updated')

        return Response(UserModelSerializer(request.user).data, status=status.HTTP_200_OK)


class ViewProfile(APIView):
    @swagger_auto_schema(responses=get_serializer_response())
    def get(self, request, **kwargs):
        """
        Get user profile info without token
        """
        user_id = self.kwargs.get('user_id')

        try:
            user_id = int(user_id)
        except Exception as ex:
            error = f'Exception in ViewProfile: {ex}'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        filter_res = User.objects.filter(id=user_id)
        if filter_res.count() == 0:
            error = 'Users not found'
            LOGGER.error(error)
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        serializer = UserModelSerializer(filter_res.first())
        return Response(serializer.sanitize(serializer.data), status=status.HTTP_200_OK)
