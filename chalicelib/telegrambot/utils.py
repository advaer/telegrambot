from datetime import datetime

from sqlalchemy import desc

from chalicelib.db.models import (
    Currency,
    Ticker,
    session,
)
from chalicelib.services.poloniex.utils import data_converter as poloniex_data_converter

from .client import api_call


def send_html_message(**kwargs):
    return api_call('sendMessage', parse_mode='HTML', **kwargs)


def get_text(key, **kwargs):
    content = {
        'start': "Hi! I am test Telegram bot, developed by <b>Rinat Advaer</b>.\n\n"
                 "/help - use it for help (as you do it now).\n\n"

                 "<b>POLONIEX tickers:</b>\n\n"

                 "/btcusd - BTC/USD ticker\n"
                 "/btceur - BTC/EUR ticker\n"
                 "/btcuah - BTC/UAH ticker\n\n"

                 "/ethusd - ETH/USD ticker\n"
                 "/etheur - ETH/EUR ticker\n"
                 "/ethuah - ETH/UAH ticker\n\n"

                 "/ltcusd - LTC/USD ticker\n"
                 "/ltceur - LTC/EUR ticker\n"
                 "/ltcuah - LTC/UAH ticker\n\n"

                 "/bchusd - BCH/USD ticker\n"
                 "/bcheur - BCH/EUR ticker\n"
                 "/bchuah - BCH/UAH ticker\n\n"

                 "/xmrusd - XMR/USD ticker\n"
                 "/xmreur - XMR/EUR ticker\n"
                 "/xmruah - XMR/UAH ticker\n\n"

                 "<b>Need a Moment?</b>\n\n"
                 "/chuck - relax from crypto currency "
                 "and get a new fact about Chuck Norris :)\n",

        'help': "<b>Available commands:\n\n</b>"

                "/start - use it to start interacting with me.\n\n"

                "<b>POLONIEX tickers:</b>\n\n"

                "/btcusd - BTC/USD ticker\n"
                "/btceur - BTC/EUR ticker\n"
                "/btcuah - BTC/UAH ticker\n\n"

                "/ethusd - ETH/USD ticker\n"
                "/etheur - ETH/EUR ticker\n"
                "/ethuah - ETH/UAH ticker\n\n"

                "/ltcusd - LTC/USD ticker\n"
                "/ltceur - LTC/EUR ticker\n"
                "/ltcuah - LTC/UAH ticker\n\n"

                "/bchusd - BCH/USD ticker\n"
                "/bcheur - BCH/EUR ticker\n"
                "/bchuah - BCH/UAH ticker\n\n"

                "/xmrusd - XMR/USD ticker\n"
                "/xmreur - XMR/EUR ticker\n"
                "/xmruah - XMR/UAH ticker\n\n"

                "<b>Need a Moment?</b>\n\n"
                "/chuck - relax from crypto currency "
                "and get a new fact about Chuck Norris :)\n",
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
