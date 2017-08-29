from .client import client


def api_call(method):
    return client.api_call(method)


def get_market(base):
    return f'USDT_{base}'


def get_ticker(response, base):
    market = get_market(base)
    return response[market]


def data_converter(data, base):
    ticker = get_ticker(data, base)
    return {
        'exchange': 'poloniex',
        'base': base,
        'counter': 'USD',
        'last': ticker['last'],
        'lowest_ask': ticker['lowestAsk'],
        'highest_bid': ticker['highestBid'],
        'percent_change': ticker['percentChange'],
        'base_volume': ticker['baseVolume'],
        'quote_volume': ticker['quoteVolume'],
        'is_frozen': ticker['isFrozen'],
        'highest_24h': ticker['high24hr'],
        'lowest_24h': ticker['low24hr'],
    }
