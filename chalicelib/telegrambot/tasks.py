from chalicelib.db.models import Currency, Ticker, session
from chalicelib.services.currencylayer.utils import api_call as currency_api_call
from chalicelib.services.poloniex.utils import api_call as poloniex_api_call
from .utils import convert_currency_to_db, convert_ticker_to_db


def get_currencies():
    counter_currencies = ['UAH', 'EUR']

    data = currency_api_call(counter_currencies)
    for counter_currency in counter_currencies:
        currency_data = convert_currency_to_db(data, counter_currency)
        session.add(Currency(**currency_data))

    session.commit()


def get_tickers(exchange='poloniex'):
    data = poloniex_api_call('returnTicker')

    base_coins = ['BTC', 'LTC', 'BCH', 'ETH', 'XMR']
    for base_coin in base_coins:
        ticker_data = convert_ticker_to_db(data, exchange, base_coin)
        session.add(Ticker(**ticker_data))

    session.commit()
