from .client import client


def api_call(method, **kwargs):
    return client.api_call(method, **kwargs)


def get_ticker(market):
    return api_call('tickers', market=market)


def get_personal_info():
    return api_call('get_personal_info')


def get_candles(market='btcuah'):
    return api_call('candles', market=market)


def get_active_orders(market='btcuah'):
    return api_call('active_orders', market=market)


def get_my_trades(market='btcuah'):
    return api_call('active_orders', market=market)
