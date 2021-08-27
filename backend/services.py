import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class ApiTotCashBack():

    api = settings.API_TOT_CASHBACK
    headers = {'token': settings.API_TOKEN}
    status_code = 0

    def get_total(self, cpf):
        response = requests.get(
            f'{self.api}/v1/cashback?cpf={cpf}',
            headers=self.headers
        )

        if not response.status_code == 200:
            logger.error(
                f'Return get_total {response.status_code}, '
                f'Reason {response.reason} '
                f'Content {response.text}'
            )
            self.status_code = response.status_code
            return {}

        self.status_code = 200
        return response.json()


class TotCashBack(ApiTotCashBack):

    def __init__(self):
        self.total_cashback = 0

    def get_total(self, cpf):
        resp = super().get_total(cpf)
        if resp:
            self.total_cashback = resp['body']['credit']
        return self
