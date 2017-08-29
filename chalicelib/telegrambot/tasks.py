from chalicelib.db.models import Currency, Ticker, session, Alert, Notification
from chalicelib.services.currencylayer.utils import \
    api_call as currency_api_call
from chalicelib.services.poloniex.utils import api_call as poloniex_api_call
from sqlalchemy import desc
from .utils import convert_currency_to_db, convert_ticker_to_db, compare
from chalicelib.telegrambot.constants import EXPRESSIONS
from chalicelib.services.poloniex.constants import CURRENCY_NAMES
import datetime
from .utils import send_html_message


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


def get_notification_content(ticker, alert):
    if alert.counter == 'USD':
        currency_rate = 1
    else:
        currency_rate, = session.query(
            Currency.last
        ).filter(
            Currency.base == 'USD', Currency.counter == alert.counter
        ).order_by(
            desc(Currency.created)).first()

    return f"ALERT!\n" \
           f"<b>\"{alert.base}/{alert.counter} {EXPRESSIONS[alert.expression]['html']} " \
           f"{float(alert.value)}\"</b>\n\n" \
           f"TICKER:\n" \
           f"<b>{alert.base}/{alert.counter} POLONIEX</b>.\n" \
           f"<b>Name:</b> {CURRENCY_NAMES[alert.base]}\n" \
           f"<b>Time:</b> UTC {ticker.created}\n\n" \
           f"<b>Last deal:</b> {ticker.last * currency_rate:.2f} {alert.counter}\n"


def process_single_alert(alert):

    if alert.counter == 'USD':
        currency_rate = 1
    else:
        currency_rate, = session.query(
            Currency.last
        ).filter(
            Currency.base == 'USD', Currency.counter == alert.counter
        ).order_by(
            desc(Currency.created)).first()

    ticker = session.query(
        Ticker
    ).filter(
        Ticker.base == alert.base,
        Ticker.counter == 'USD'
    ).order_by(
        desc(Ticker.created)
    ).first()

    if compare(ticker.last * currency_rate, alert.value) in EXPRESSIONS[alert.expression]['result']:
        notifications = session.query(
            Notification
        ).filter(
            Notification.alert_id == alert.id,
            Notification.created >= datetime.datetime.utcnow() - datetime.timedelta(minutes=10)
        ).count()

        if not notifications:
            content = get_notification_content(ticker, alert)
            response = send_html_message(chat_id=alert.chat.telegram_chat_id, content=content)
            if response.status_code == 200:
                session.add(
                    Notification(
                        alert=alert
                    )
                )
                session.commit()


def process_all_alerts():
    alerts = session.query(Alert).filter(Alert.is_active == 1).all()
    for alert in alerts:
        process_single_alert(alert)
