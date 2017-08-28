from functools import partial

import requests
from sqlalchemy import desc

from chalicelib.db.models import Currency, Ticker, session, Chat
from chalicelib.services.poloniex.constants import CURRENCY_NAMES


class BotCommands:
    def __init__(self):
        self.known_commands = {
            '/start': self.start,
            '/help': partial(self.get_text, data=None, args=None, key='help'),
            '/chuck': self.get_chuck_quote,

            '/btcusd': partial(self.ticker, data=None, args=None, base='BTC', counter='USD'),
            '/btceur': partial(self.ticker, data=None, args=None, base='BTC', counter='EUR'),
            '/btcuah': partial(self.ticker, data=None, args=None, base='BTC', counter='UAH'),

            '/ethusd': partial(self.ticker, data=None, args=None, base='ETH', counter='USD'),
            '/etheur': partial(self.ticker, data=None, args=None, base='ETH', counter='EUR'),
            '/ethuah': partial(self.ticker, data=None, args=None, base='ETH', counter='UAH'),

            '/ltcusd': partial(self.ticker, data=None, args=None, base='LTC', counter='USD'),
            '/ltceur': partial(self.ticker, data=None, args=None, base='LTC', counter='EUR'),
            '/ltcuah': partial(self.ticker, data=None, args=None, base='LTC', counter='UAH'),

            '/bchusd': partial(self.ticker, data=None, args=None, base='BCH', counter='USD'),
            '/bcheur': partial(self.ticker, data=None, args=None, base='BCH', counter='EUR'),
            '/bchuah': partial(self.ticker, data=None, args=None, base='BCH', counter='UAH'),

            '/xmrusd': partial(self.ticker, data=None, args=None, base='XMR', counter='USD'),
            '/xmreur': partial(self.ticker, data=None, args=None, base='XMR', counter='EUR'),
            '/xmruah': partial(self.ticker, data=None, args=None, base='XMR', counter='UAH'),
        }

    def start(self, **kwargs):
        chat = kwargs['data']['message']['chat']
        chat_id = chat.get('id')
        if not session.query(Chat).filter(Chat.chat_id == chat_id).count():
            session.add(Chat(
                chat_id=chat_id,
                chat_type=chat.get('type'),
                title=chat.get('title'),
                username=chat.get('username'),
                first_name=chat.get('first_name'),
                last_name=chat.get('last_name'),
                all_members_are_administrators=chat.get('all_members_are_administrators'),
                description=chat.get('description'),
                invite_link=chat.get('invite_link'),
                created_at=chat.get('created_at'),
            ))
            session.commit()
        text = self.get_text('start')
        return text

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
    def ticker(base, counter, **kwargs):

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
            'currency_name': CURRENCY_NAMES.get(base),
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
                       "<b>Name:</b> {currency_name}\n"
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
