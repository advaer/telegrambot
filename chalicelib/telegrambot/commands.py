import requests
from chalicelib.kunatrade.utils import get_ticker
import functools

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
            '/btc': functools.partial(self.get_ticker, market='btcuah'),
            '/eth': functools.partial(self.get_ticker, market='ethuah')
        }

    @staticmethod
    def get_text(key):
        content = {
            'start': "Hi! I am test Telegram bot, developed by <b>Rinat Advaer</b>.\n"
                     "/help - use it for help.\n"
                     "/chuck - get new fact about Chuck Norris.\n"
                     "/btc - KUNA BTC/UAH ticker info.\n"
                     "/eth - KUNA ETH/UAH ticker info.\n",

            'help': "Not much to do here for now\n"
                     "/chuck - get new fact about Chuck Norris.\n" 
                     "/btc - KUNA BTC ticker info.\n"
                     "/eth - KUNA ETH/UAH ticker info.\n"
        }
        return content.get(key)

    @staticmethod
    def get_chuck_quote():
        quote = requests.get('https://api.chucknorris.io/jokes/random')
        return quote.json().get('value')

    @staticmethod
    def get_ticker(market):
        data = get_ticker(market)
        market_buy, market_sell = kuna_markets.get(market).split('/')
        ticker_data = {key: float(value) for key, value in data.get('ticker').items()}
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
        return response_template.get('content').format(market_buy, market_sell, **ticker_data)

    @staticmethod
    def default():
        return "Oops... I don't know this command. Try again!"


commands = BotCommands()
