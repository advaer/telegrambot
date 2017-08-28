from datetime import datetime

from chalicelib.services.poloniex.utils import get_ticker as get_poloniex_ticker
from .client import api_call


def send_html_message(**kwargs):
    return api_call('sendMessage', parse_mode='HTML', **kwargs)


def poloniex_converter(data, base):
    ticker = get_poloniex_ticker(data, base)
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


def convert_ticker_to_db(data, exchange, base):

    exchange_converters = {
        'poloniex': poloniex_converter,
    }

    converter = exchange_converters[exchange]

    return converter(data, base)


def convert_currency_to_db(data, counter):
    rate = data['quotes'][f'USD{counter}']
    created_at = datetime.utcfromtimestamp(data['timestamp'])
    return {
        'base': 'USD',
        'counter': counter,
        'last': rate,
        'created_at': created_at
    }
