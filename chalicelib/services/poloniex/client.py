import requests

API_METHODS = {
    'public': [
        'returnTicker',
    ],
    'private': [

    ],
}


class PoloniexClient:
    def __init__(self):
        self.public_api_url = 'https://poloniex.com/public'

    def _make_request(self, api_method):
        if api_method in API_METHODS['public']:
            data = {
                'command': api_method,
            }
            return requests.get(self.public_api_url, data)
        else:
            raise NotImplementedError

    def api_call(self, api_method):
        response = self._make_request(api_method)
        return response.json()


client = PoloniexClient()
