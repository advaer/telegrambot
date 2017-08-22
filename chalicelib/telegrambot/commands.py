import functools

import requests
from sqlalchemy import desc

from chalicelib.db.models import CurrencyRate, session
from chalicelib.kunatrade.utils import get_ticker

kuna_markets = {
    'btcuah': 'BTC/UAH',
    'ethuah': 'ETH/UAH'
}


class BotCommands:
    def __init__(self):
        self.known_commands = {
            '/start': functools.partial(self.get_text, 'start'),
            '/help': functools.partial(self.get_text, 'help'),
            '/chuck': self.get_chuck_quote,
            '/btcuah': functools.partial(self.ticker, market='btcuah', currency='UAH'),
            '/btcusd': functools.partial(self.ticker, market='btcuah', currency='USD'),
            '/btceur': functools.partial(self.ticker, market='btcuah', currency='EUR'),
            '/ethuah': functools.partial(self.ticker, market='ethuah', currency='UAH'),
            '/ethusd': functools.partial(self.ticker, market='ethuah', currency='USD'),
            '/etheur': functools.partial(self.ticker, market='ethuah', currency='EUR'),
        }

    @staticmethod
    def get_text(key):
        content = {
            'start': "Hi! I am test Telegram bot, developed by <b>Rinat Advaer</b>.\n\n"
                     "/help - use it for help (as you do it now).\n\n"

                     "/btcuah - KUNA BTC/UAH ticker\n"
                     "/btcusd - KUNA BTC/USD ticker\n"
                     "/btceur - KUNA BTC/EUR ticker\n\n"
                     "/ethuah - KUNA ETH/UAH ticker\n"
                     "/ethusd - KUNA ETH/USD ticker\n"
                     "/etheur - KUNA ETH/EUR ticker\n\n"

                     "/chuck - get relaxed from crypto currency "
                     "and get new fact about Chuck Norris :)\n",

            'help': "<b>Available commands:\n\n</b>"
                    "/start - use it to start interacting with me.\n"
                    "/help - use it for help (as you do it now).\n\n"

                    "/btcuah - KUNA BTC/UAH ticker\n"
                    "/btcusd - KUNA BTC/USD ticker\n"
                    "/btceur - KUNA BTC/EUR ticker\n\n"
                    "/ethuah - KUNA ETH/UAH ticker\n"
                    "/ethusd - KUNA ETH/USD ticker\n"
                    "/etheur - KUNA ETH/EUR ticker\n\n"

                    "/chuck - get relaxed from Crypto and "
                    "get a new fact about Chuck Norris :)\n"
        }
        return content.get(key)

    @staticmethod
    def get_chuck_quote():
        quote = requests.get('https://api.chucknorris.io/jokes/random')
        return quote.json().get('value')

    @staticmethod
    def ticker(market, currency):

        if currency == 'UAH':
            currency_rate = 1
        else:
            currency_rate, = session.query(
                CurrencyRate.rate
            ).filter(
                CurrencyRate.base_currency == currency, CurrencyRate.counter_currency == 'UAH'
            ).order_by(
                desc(CurrencyRate.created_at)).first()

        data = get_ticker(market)
        market_buy, market_sell = kuna_markets.get(market).split('/')

        ticker = data.get('ticker')
        ticker_data = {
            'buy': float(ticker.get('buy'))/currency_rate,
            'sell': float(ticker.get('sell'))/currency_rate,
            'low': float(ticker.get('low'))/currency_rate,
            'high': float(ticker.get('high'))/currency_rate,
            'last': float(ticker.get('last'))/currency_rate,
            'vol': float(ticker.get('vol')),
            'price': float(ticker.get('price'))/currency_rate,
        }
        response_template = {
            'content': "<b>Market: {0}/{1} KUNA Exchange</b>.\n\n"
                       "<b>Buy:</b> {buy:.2f} {1}\n"
                       "<b>Sell</b>: {sell:.2f} {1}\n"
                       "<b>Last deal price:</b> {last:.2f} {1}\n"
                       "<b>Lowest in 24h:</b> {low:.2f} {1}\n"
                       "<b>Highest in 24h:</b> {high:.2f} {1}\n"
                       "<b>Trading vol. 24h:</b> {vol} {0}\n"
                       "<b>Trading vol. 24h:</b> {price:.2f} {1}"
        }
        return response_template.get('content').format(market_buy, currency, **ticker_data)

    @staticmethod
    def default():
        return "Oops... I don't know this command. Try again!"


commands = BotCommands()
