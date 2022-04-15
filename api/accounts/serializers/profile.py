import re

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from rest_framework import serializers

from api.accounts import LOGGER
from api.accounts.models.profile import User
from api.parallel.management.commands.inn_verification import check_smz_by_inn


def separate_username_from_url(url: str) -> str:
    splitted = url.split('/')
    for part in splitted[::-1]:
        if part != '':
            return part


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'image_url',
            'gender',
            'phone',
            'address',
            'occupation',
            'inn',
            'vk',
            'instagram',
            'facebook',
            'website',
            'verified',
        ]

    def validate(self, data: dict) -> dict:
        # Prevent email address from being changed
        if 'email' in data:
            del data['email']

        # These fields are either None or str
        strfields = [
            'phone',
            'inn',
            'vk',
            'instagram',
            'facebook',
            'website'
        ]

        for field in strfields:
            if field in data:
                value = data[field]
                if value is not None and type(value) != str:
                    error = f'{field} must be str or null'
                    LOGGER.error(error)
                    raise serializers.ValidationError(error)

        # Phone format check
        if data.get('phone') is not None and data['phone'] != '':
            phone_reg = re.compile(r'^\+?\d{11}$')
            if re.fullmatch(phone_reg, data['phone']) is None:
                error = 'Phone number must be entered in the format: +71234567890'
                LOGGER.error(error)
                raise serializers.ValidationError(error)

        # 12-digit number
        if data.get('inn') is not None and data['inn'] != '':
            inn_reg = re.compile(r'^(\d{12})$')
            if re.fullmatch(inn_reg, data['inn']) is None:
                error = 'INN must be a 12-digit number'
                LOGGER.error(error)
                raise serializers.ValidationError(error)
            data['verified'] = check_smz_by_inn(data['inn'])

        # Username is either given entirely or as a substring of a link (xxx://xxx.xxx.xxx/xxx/username)
        # So, we are looking for the string after the last slash (if it exists) that matches the regex

        # id0123456789 or username
        if data.get('vk') is not None and data['vk'] != '':
            data['vk'] = separate_username_from_url(data['vk'])
            vk_reg = re.compile(r'^(id(\d{9})|[a-zA-Z][a-zA-Z0-9_.]+)$')
            if re.fullmatch(vk_reg, data['vk']) is None:
                error = 'Invalid VK username'
                LOGGER.error(error)
                raise serializers.ValidationError(error)

        # https://regexr.com/3cg7r
        if data.get('instagram') is not None and data['instagram'] != '':
            data['instagram'] = separate_username_from_url(data['instagram'])
            inst_reg = re.compile(r'^(?!.*\.\.)(?!.*\.$)[^\W][\w.]{0,29}$')
            if re.fullmatch(inst_reg, data['instagram']) is None:
                error = 'Invalid Instagram username'
                LOGGER.error(error)
                raise serializers.ValidationError(error)

        # https://stackoverflow.com/a/4330466
        if data.get('facebook') is not None and data['facebook'] != '':
            data['facebook'] = separate_username_from_url(data['facebook'])
            fb_reg = re.compile(r'^[a-z\d.]{5,}$')
            if re.fullmatch(fb_reg, data['facebook']) is None:
                error = 'Invalid Facebook username'
                LOGGER.error(error)
                raise serializers.ValidationError(error)

        # https://stackoverflow.com/a/7160819
        if data.get('website') is not None and data['website'] != '':
            url_val = URLValidator()
            to_check = data['website']
            if not to_check.startswith('https://') and not to_check.startswith('http://'):
                to_check = 'https://' + to_check
            try:
                url_val(to_check)
            except ValidationError as ex:
                error = f'Invalid website due to {ex}'
                LOGGER.error(error)
                raise serializers.ValidationError(error)

        return data

    def sanitize(self, data: dict) -> dict:
        if 'email' in data:
            del data['email']
        if 'inn' in data:
            del data['inn']
        return data

    def update(self, instance, validated_data: dict):
        return serializers.ModelSerializer.update(self, instance, validated_data)
