import functools

import requests
from sqlalchemy import desc

from chalicelib.db.models import Currency, Ticker, session


class BotCommands:
    def __init__(self):
        self.known_commands = {
            '/start': functools.partial(self.get_text, 'start'),
            '/help': functools.partial(self.get_text, 'help'),
            '/chuck': self.get_chuck_quote,

            '/btcusd': functools.partial(self.ticker, base='BTC', counter='USD'),
            '/btceur': functools.partial(self.ticker, base='BTC', counter='EUR'),
            '/btcuah': functools.partial(self.ticker, base='BTC', counter='UAH'),

            '/ethusd': functools.partial(self.ticker, base='ETH', counter='USD'),
            '/etheur': functools.partial(self.ticker, base='ETH', counter='EUR'),
            '/ethuah': functools.partial(self.ticker, base='ETH', counter='UAH'),

            '/ltcusd': functools.partial(self.ticker, base='LTC', counter='USD'),
            '/ltceur': functools.partial(self.ticker, base='LTC', counter='EUR'),
            '/ltcuah': functools.partial(self.ticker, base='LTC', counter='UAH'),

            '/bchusd': functools.partial(self.ticker, base='BCH', counter='USD'),
            '/bcheur': functools.partial(self.ticker, base='BCH', counter='EUR'),
            '/bchuah': functools.partial(self.ticker, base='BCH', counter='UAH'),

            '/xmrusd': functools.partial(self.ticker, base='XMR', counter='USD'),
            '/xmreur': functools.partial(self.ticker, base='XMR', counter='EUR'),
            '/xmruah': functools.partial(self.ticker, base='XMR', counter='UAH'),
        }

    @staticmethod
    def get_text(key):
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

    @staticmethod
    def get_chuck_quote():
        quote = requests.get('https://api.chucknorris.io/jokes/random')
        return quote.json().get('value')

    @staticmethod
    def ticker(base, counter):

        if counter == 'USD':
            currency_rate = 1
        else:
            currency_rate, = session.query(
                Currency.last
            ).filter(
                Currency.base == 'USD', Currency.counter == counter
            ).order_by(
                desc(Currency.created_at)).first()

        ticker = session.query(
            Ticker
        ).filter(
            Ticker.base == base, Ticker.counter == 'USD'
        ).order_by(
            desc(Ticker.created_at)).first()

        ticker_data = {
            'created_at': ticker.created_at,
            'lowest_ask': ticker.lowest_ask * currency_rate,
            'highest_bid': ticker.highest_bid * currency_rate,
            'last': ticker.last * currency_rate,
            'lowest_24h': ticker.lowest_24h * currency_rate,
            'highest_24h': ticker.lowest_24h * currency_rate,
            'quote_volume': ticker.quote_volume,
            'base_volume': ticker.base_volume * currency_rate,
        }

        response_template = {
            'content': "<b>{0}/{1} POLONIEX</b>.\n"
                       "<b>Time:</b> UTC {created_at}\n\n"
                       "<b>Lowest Ask:</b> {lowest_ask:.2f} {1}\n"
                       "<b>Highest Bid:</b> {highest_bid:.2f} {1}\n"
                       "<b>Last deal:</b> {last:.2f} {1}\n"
                       "<b>Lowest in 24h:</b> {lowest_24h:.2f} {1}\n"
                       "<b>Highest in 24h:</b> {highest_24h:.2f} {1}\n"
                       "<b>Trading vol. 24h:</b> {quote_volume:.2f} {0}\n"
                       "<b>Trading vol. 24h:</b> {base_volume:.2f} {1}\n"
        }
        return response_template.get('content').format(base, counter, **ticker_data)

    @staticmethod
    def default():
        return "Oops... I don't know this command. Try again or use /help"


commands = BotCommands()
