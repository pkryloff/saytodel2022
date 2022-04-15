import random

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_fuzzysearch.search import RankedFuzzySearchFilter

from api.accounts.models.profile import User
from api.crm import LOGGER
from api.marketplace.schemas import get_response, get_schema
from api.mysite.models.site import MySite
from .utils import StringTransformer


class Marketplace(APIView, RankedFuzzySearchFilter):
    @swagger_auto_schema(manual_parameters=get_schema, responses=get_response)
    def get(self, request):
        """
        Get cards info with user's sites
        """
        offset = int(request.query_params.get('offset', 0))
        limit = int(request.query_params.get('limit', 20))
        search_term = str(request.query_params.get('search_term', ''))
        min_rank = float(request.query_params.get('min_rank', 0.0))
        search_fields = ('first_name', 'last_name', 'address', 'occupation')
        transformer = StringTransformer()
        cards = list()

        if search_term != '':
            queryset = User.objects.all()
            all_terms = [
                search_term,
                transformer.transform_by_translit(search_term, 'ru'),
                transformer.transform_by_translit(search_term, 'en'),
                transformer.transform_by_layout(search_term, 'ru'),
                transformer.transform_by_layout(search_term, 'en')
            ]
            search_result = None
            for term in all_terms:
                if search_result is None:
                    search_result = self.search_queryset(queryset, search_fields, term,
                                                         min_rank=min_rank)
                else:
                    search_result = search_result | self.search_queryset(queryset, search_fields, term,
                                                                         min_rank=min_rank)
            search_result = list(search_result.order_by('-rank'))
        else:
            verified = list(User.objects.filter(verified=True))
            other = list(User.objects.filter(verified=False))
            random.seed(0)
            random.shuffle(verified)
            random.shuffle(other)
            search_result = verified + other

        for user in search_result:
            if MySite.objects.filter(owner_id=user.id).count() == 0:
                continue
            info = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'occupation': user.occupation,
                'image_url': user.image_url,
                'address': user.address,
                'verified': user.verified,
                'site_name': MySite.objects.filter(owner_id=user.id).first().name,
            }
            cards.append(info)

        LOGGER.info(f'Cards info retrieved')
        return Response(cards[offset:offset + limit], status=status.HTTP_200_OK)
