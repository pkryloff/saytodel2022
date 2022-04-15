import json
from typing import List, Tuple

from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from Samodelkin.middlewares import LOGGER
from Samodelkin.settings import BASE_DIR


def flatten_data(obj) -> List[str]:
    user_inputs = []
    if isinstance(obj, dict):
        for value in list(obj.values()):
            user_inputs.extend(flatten_data(value))
    elif isinstance(obj, list):
        for value in obj:
            user_inputs.extend(flatten_data(value))
    elif isinstance(obj, str):
        user_inputs.extend(obj.lower().split())
    return user_inputs


def is_censored(inputs: List[str]) -> Tuple[bool, List[str]]:
    blacklist_path = str(BASE_DIR / 'Samodelkin/middlewares/blacklist.txt')
    blacklist = open(blacklist_path, 'r').read().splitlines()
    bad_words = list(set(inputs).intersection(set(blacklist)))
    if len(bad_words) != 0:
        return False, bad_words
    return True, bad_words


class CensorshipMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not (request.path.startswith('/api/') and
                request.method in ('POST', 'PUT') and
                request.META.get('CONTENT_TYPE') == 'application/json'):
            return None

        data = json.loads(request.body)
        user_inputs = flatten_data(data)
        checker_flag, bad_words = is_censored(user_inputs)

        if not checker_flag:
            msg = 'Data contains profanity'
            LOGGER.info(f'{msg}, word {bad_words[0]}')
            response = Response(
                {'msg': msg, 'bad_word': bad_words[0]},
                content_type='application/json',
                status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
            )
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = 'application/json'
            response.renderer_context = {}
            return response.render()
        return None
