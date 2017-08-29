from functools import partial

import requests
from chalice import Chalice

from chalicelib.db.models import (
    Alert,
    Chat,
    session,
)
from chalicelib.services.poloniex.constants import CURRENCY_NAMES
from chalicelib.telegrambot.constants import EXPRESSIONS

from .utils import (
    get_currency_rate,
    get_latest_ticker,
    get_text,
)

app = Chalice(app_name='advaerbot')


class BotCommands:
    def __init__(self):
        self.known_commands = {
            '/start': self.start,
            '/help': partial(get_text, data=None, args=None, key='help'),
            '/chuck': self.get_chuck_quote,

            '/setalert': self.setalert,
            '/alerts': self.alerts,
            '/stopalert': self.stopalert,

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

    @staticmethod
    def start(data, **kwargs):
        chat = data['message']['chat']
        chat_id = chat.get('id')
        if not session.query(Chat).filter(
                        Chat.telegram_chat_id == chat_id
        ).count():
            session.add(Chat(
                telegram_chat_id=chat_id,
                chat_type=chat.get('type'),
                title=chat.get('title'),
                username=chat.get('username'),
                first_name=chat.get('first_name'),
                last_name=chat.get('last_name'),
                all_members_are_administrators=chat.get(
                    'all_members_are_administrators'
                ),
                description=chat.get('description'),
                invite_link=chat.get('invite_link'),
                created=chat.get('created'),
            ))
            session.commit()
        return get_text('start')

    @staticmethod
    def get_chuck_quote(**kwargs):
        quote = requests.get('https://api.chucknorris.io/jokes/random')
        return quote.json().get('value')

    @staticmethod
    def ticker(base, counter, **kwargs):
        currency_rate = get_currency_rate(counter)
        ticker = get_latest_ticker(base)

        ticker_data = {
            'created': ticker.created,
            'currency_name': CURRENCY_NAMES.get(base),
            'lowest_ask': ticker.lowest_ask * currency_rate,
            'highest_bid': ticker.highest_bid * currency_rate,
            'last': ticker.last * currency_rate,
            'lowest_24h': ticker.lowest_24h * currency_rate,
            'highest_24h': ticker.highest_24h * currency_rate,
            'quote_volume': ticker.quote_volume,
            'base_volume': ticker.base_volume * currency_rate,
        }

        response_template = {
            'content': "<b>{0}/{1} POLONIEX</b>.\n"
                       "<b>Name:</b> {currency_name}\n"
                       "<b>Time:</b> UTC {created}\n\n"
                       "<b>Lowest Ask:</b> {lowest_ask:.2f} {1}\n"
                       "<b>Highest Bid:</b> {highest_bid:.2f} {1}\n"
                       "<b>Last deal:</b> {last:.2f} {1}\n"
                       "<b>Lowest in 24h:</b> {lowest_24h:.2f} {1}\n"
                       "<b>Highest in 24h:</b> {highest_24h:.2f} {1}\n"
                       "<b>Trading vol. 24h:</b> {quote_volume} {0}\n"
                       "<b>Trading vol. 24h:</b> {base_volume:.2f} {1}\n"
        }
        return response_template.get('content').format(
            base, counter, **ticker_data
        )

    @staticmethod
    def setalert(data, args):

        if not args:
            return "Please provide arguments"

        chat_id = data['message']['chat']['id']
        chat = session.query(Chat).filter(
            Chat.telegram_chat_id == chat_id
        ).one_or_none()
        try:
            base, counter, expression, value = args
        except ValueError:
            return "Incorrect args.\nExample: <b>BTC UAH > 123456</b>"

        base = base.upper()
        if base not in CURRENCY_NAMES.keys():
            return f"Base currency is incorrect. Allowed: {CURRENCY_NAMES.keys()}"

        counter = counter.upper()
        if counter not in ['USD', 'EUR', 'UAH']:
            return f"Counter currency is incorrect. Allowed: ['USD', 'EUR', 'UAH']"

        if expression not in EXPRESSIONS.keys():
            return f"Expression is incorrect."

        try:
            value = float(value)
        except ValueError:
            return f"Value is incorrect. It should be 12345 or 123.45"

        session.add(
            Alert(
                chat=chat,
                base=base,
                counter=counter,
                expression=expression,
                value=value
            )
        )
        session.commit()
        return f"Alert <b>\"{base}/{counter} " \
               f"{EXPRESSIONS[expression]['html']} {value}\"</b>" \
               f" has been set successfully"

    @staticmethod
    def alerts(data, **kwargs):
        app.log.debug('Logs in chalicelib works well')
        telegram_chat_id = data['message']['chat']['id']

        chat = session.query(Chat).filter(
            Chat.telegram_chat_id == telegram_chat_id
        ).one()

        alerts = session.query(Alert).filter(
            Alert.chat == chat,
            Alert.is_active == 1
        ).all()

        if not alerts:
            return "There are no active alerts. Use /setalert to create"

        content = "ACTIVE ALERTS:\n\n"
        for alert in alerts:
            content += f"<b>Alert id: {alert.id}</b>\n" \
                       f"{alert.base}/{alert.counter} {EXPRESSIONS[alert.expression]['html']} " \
                       f"{float(alert.value)}\n\n"
        return content

    @staticmethod
    def stopalert(data, args):

        if not args:
            return "Please provide arguments"

        alert = session.query(Alert).filter(Alert.id == args[0]).one_or_none()

        if alert and alert.chat.telegram_chat_id \
                == data['message']['chat']['id']:
            alert.is_active = False
            session.add(alert)
            session.commit()
            return f"STOPPED!\n" \
                   f"Alert id: {alert.id}\n" \
                   f"{alert.base}/{alert.counter} {EXPRESSIONS[alert.expression]['html']} " \
                   f"{float(alert.value)}\n\n"
        else:
            return "Incorrect alert ID. " \
                   "To list all active alerts with IDs use /alerts"

    @staticmethod
    def default(**kwargs):
        return "Oops... I don't know this command. Try again or use /help"


commands = BotCommands()
