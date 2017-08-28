from .client import client


def api_call(method):
    return client.api_call(method)


def get_market(base):
    return f'USDT_{base}'


def get_ticker(response, base):
    market = get_market(base)
    return response[market]
