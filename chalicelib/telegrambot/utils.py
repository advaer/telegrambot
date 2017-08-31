from datetime import datetime

from sqlalchemy import desc

from chalicelib.db.models import (
    Currency,
    Ticker,
    session,
)
from chalicelib.services.poloniex.utils import data_converter as poloniex_data_converter

from .client import api_call
from .constants import MAIN_MENU


def send_html_message(**kwargs):
    return api_call('sendMessage', parse_mode='HTML', **kwargs)


def get_text(key, **kwargs):

    content = {
        'start': f"Hi! I am Telegram bot, developed by @advaer.\n"
                 f"/help - use it for help\n"
                 f"{MAIN_MENU}",

        'help': f"<b>Available commands:\n</b>"
                f"/start - use it to start interacting with me\n"
                f"{MAIN_MENU}"
    }
    return content.get(key)


def convert_ticker_to_db(data, exchange, base):

    exchange_converters = {
        'poloniex': poloniex_data_converter,
    }

    converter = exchange_converters[exchange]

    return converter(data, base)


def convert_currency_to_db(data, counter):
    rate = data['quotes'][f'USD{counter}']
    created = datetime.utcfromtimestamp(data['timestamp'])
    return {
        'base': 'USD',
        'counter': counter,
        'last': rate,
        'created': created
    }


def compare(x, y):
    if x == y:
        return 0
    return int((x - y)/abs(x - y))


def get_currency_rate(counter):
    if counter == 'USD':
        currency_rate = 1
    else:
        currency_rate, = session.query(
            Currency.last
        ).filter(
            Currency.base == 'USD', Currency.counter == counter
        ).order_by(
            desc(Currency.created)).first()
    return currency_rate


def get_latest_ticker(base):
    return session.query(
        Ticker
    ).filter(
        Ticker.base == base,
        Ticker.counter == 'USD'
    ).order_by(
        desc(Ticker.created)
    ).first()
