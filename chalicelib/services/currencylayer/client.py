import requests

from chalicelib.conf import settings


class CurrencyLayerClient:
    def __init__(self):
        self.api_url = 'http://www.apilayer.net/api/live'

    def api_cal(self, currencies):
        data = {
            'access_key': settings.CURRENCY_ACCESS_KEY,
            'currencies': ','.join(currencies)
        }
        response = requests.get(self.api_url, params=data)
        return response.json()


client = CurrencyLayerClient()
