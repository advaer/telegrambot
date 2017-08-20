import requests
from chalicelib.kunatrade.utils import ticker_btc


class BotCommands:
    def __init__(self):
        self.known_commands = {
            '/start': self._get_static_text,
            '/help': self._get_static_text,
            '/chuck': self._get_chuck_quote,
            '/btc': self._get_btc_ticker,
        }

    def _get_chuck_quote(self, **kwargs):
        quote = requests.get('https://api.chucknorris.io/jokes/random')
        return quote.json().get('value')

    def _get_static_text(self, **kwargs):
        TEXT = {
            '/start': "Hi! I am test Telegram bot, developed by <b>Rinat Advaer</b>.\n"
                      "/help - use it for help.\n"
                      "/chuck - get new fact about Chuck Norris.\n"
                      "/btc - KUNA BTC ticker info.\n"
                      "For any other questions, please contact my creator: @advaer",
            '/help': "Not much to do here for now\n"
                     "/chuck - get new fact about Chuck Norris.\n"
                     "/btc - KUNA BTC ticker info.\n"
        }
        return TEXT[kwargs['key']]

    def _get_btc_ticker(self, **kwargs):

        markets = {
            'btcuah': 'BTC/UAH'
        }
        data = ticker_btc()
        message_data = [
            markets.get(data.get('market')),
            round(float(data.get('ticker').get('buy')), 2),
            round(float(data.get('ticker').get('sell')), 2),
            round(float(data.get('ticker').get('last')), 2),
            round(float(data.get('ticker').get('low')), 2),
            round(float(data.get('ticker').get('high')), 2),
            data.get('ticker').get('vol'),
            round(float(data.get('ticker').get('price')), 2)
        ]
        message = "<b>Market: {} KUNA Exchange</b>.\n\n<b>Buy:</b> {:.2f} UAH\n" \
                  "<b>Sell</b>: {:.2f} UAH\n<b>Last deal price:</b> {:.2f} UAH\n" \
                  "<b>Lowest in 24h:</b> {:.2f} UAH\n<b>Highest in 24h:</b> {:.2f} UAH\n" \
                  "<b>Trading vol. 24h:</b> {} BTC\n" \
                  "<b>Trading vol. 24h:</b> {:.2f} UAH".format(*message_data)
        return message


class BotProcessing:
    def __init__(self):
        self.commands = BotCommands()

    def process(self, data):
        request = data.get("message").get('text')
        chat_id = data.get("message").get('chat').get('id')
        command = self.commands.known_commands.get(request)
        response_text = "Oops... I don't know this command. Try again!"

        if command:
            response_text = command(key=request)

        r = requests.post(
            'https://api.telegram.org/bot385440215:AAEBzlx5FLSJ6m8aF2CrQtl0NIy7oR1YDqQ/sendMessage',
            data={
                "chat_id": chat_id,
                "parse_mode": "HTML",
                "text": response_text
            }
        )
        return {'status': r.status_code}
