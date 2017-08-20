from .client import client


def api_call(method, **kwargs):
    return client.api_call(method, **kwargs)


def ticker_btc():
    market = 'btcuah'
    response = api_call('tickers', market=market)
    response['market'] = market
    return response


def ticker_gol():
    market = 'golbtc'
    response = api_call('tickers', market=market)
    response['market'] = market
    return response


def ticker_eth():
    market = 'ethuah'
    response = api_call('tickers', market=market)
    response['market'] = market
    return response


def ticker_waves():
    market = 'wavesuah'
    response = api_call('tickers', market=market)
    response['market'] = market
    return response


def ticker_kun():
    market = 'kunbtc'
    response = api_call('tickers', market=market)
    response['market'] = market
    return response


def ticker_bch():
    market = 'bchbtc'
    response = api_call('tickers', market=market)
    response['market'] = market
    return response


def personal_info():
    return api_call('get_personal_info')


def candles_btc():
    market = 'btcuah'
    return api_call('candles', market=market)


def active_orders_btc():
    market = 'btcuah'
    return api_call('active_orders', market=market)


def my_trades_btc():
    market = 'btcuah'
    return api_call('active_orders', market=market)