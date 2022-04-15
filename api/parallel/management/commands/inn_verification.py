import time
from datetime import date

import requests
import schedule
from django.core.management.base import BaseCommand

from api.accounts.models.profile import User
from api.parallel import LOGGER

FNS_API_URL = 'https://statusnpd.nalog.ru:443/api/v1/tracker/taxpayer_status'


def check_smz_by_inn(inn: str):
    try:
        data = {'inn': inn, 'requestDate': str(date.today())}
        r = requests.post(FNS_API_URL, json=data, timeout=90).json()

        error_code = r.get('code')
        if error_code is not None:
            LOGGER.error(f'Error while check {inn} inn: {r.get("message")}')

            if error_code == 'taxpayer.status.service.limited.error':
                time.sleep(120)
                r = requests.post(FNS_API_URL, json=data, timeout=90).json()

    except requests.Timeout:
        LOGGER.error(f'No response from API while check {inn} inn')
    except Exception as e:
        LOGGER.error(f'Exception caused while check {inn} inn: {e}')
    else:
        return r.get('status', False)
    return False


def inn_verification():
    LOGGER.info('Run inn checking...')
    for user in User.objects.all():
        if user.inn is None or user.inn == '':
            user.verified = False
            user.save()
        else:
            user.verified = check_smz_by_inn(user.inn)
            user.save()
            time.sleep(60)
    LOGGER.info('All users checked')


schedule.every().day.at('03:00').do(inn_verification)


class Command(BaseCommand):
    help = 'INN confirmation'

    def handle(self, *args, **options):
        LOGGER.info('Inn checker started')
        while True:
            schedule.run_pending()
            time.sleep(60)
