import requests
import hmac
import time
import hashlib
import collections

from . import settings


class KunaClient:

    def __init__(self, settings):
        self.BASE_API_URL = settings.BASE_API_URL
        self.PUBLIC_KEY = settings.PUBLIC_KEY
        self.SECRET_KEY = settings.SECRET_KEY
        self.API_SPEC = settings.API_SPEC

    def get_api_method(self, method):
        return self.API_SPEC.get(method)

    @staticmethod
    def get_verb(api_method):
        return api_method.get('verb')

    @staticmethod
    def get_path(api_method, **kwargs):
        if api_method.get('market_path'):
            return '{0}/{1}'.format(api_method.get('path'), kwargs['market'])
        return api_method.get('path')

    @staticmethod
    def is_private(api_method):
        return api_method.get('is_private')

    @staticmethod
    def make_request(verb, url, data):
        r = None
        if verb == 'GET':
            r = requests.get(url, params=data)
        if verb == 'POST':
            r = requests.post(url, data=data)
        return r

    def get_signature(self, verb, path, params):
        secret = self.SECRET_KEY.encode()

        data = '{0}|{1}|'.format(verb, path)
        for k, v in params.items():
            data += '{0}={1}&'.format(k, v)
        data = data[:-1].encode()
        return hmac.new(secret, data, hashlib.sha256).hexdigest()

    def get_params(self, private, **kwargs):
        timestamp = int(time.time()*1000)
        auth_params = {}
        if private:
            auth_params = {
                'access_key': self.PUBLIC_KEY,
                'tonce': timestamp,
            }
        data_params = kwargs
        result = {}
        result.update(auth_params.copy())
        result.update(data_params.copy())
        result = collections.OrderedDict(sorted(result.items()))
        return result

    def get_request_data(self, verb, path, private, **kwargs):
        params = self.get_params(private, **kwargs)
        if private:
            params.update({'signature': self.get_signature(verb, path, params)})
        return params

    def api_call(self, method, **kwargs):
        api_method = self.get_api_method(method)

        verb = self.get_verb(api_method)
        path = self.get_path(api_method, **kwargs)
        private = self.is_private(api_method)

        data = self.get_request_data(verb, path, private, **kwargs)

        url = '{0}{1}'.format(self.BASE_API_URL, path)
        r = self.make_request(verb, url, data)

        return r.json()


client = KunaClient(settings)
