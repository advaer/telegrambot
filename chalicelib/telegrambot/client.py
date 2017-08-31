import requests

from chalicelib.conf import settings


class TelegramBotClient:

    def __init__(self):
        self.bot_url = 'https://api.telegram.org/bot'

    def api_call(self, method_name, parse_mode, **data):
        url = f'{self.bot_url}{settings.TELEGRAM_BOT_TOKEN}/{method_name}'
        response = requests.post(
            url,
            data={
                "chat_id": data.get('chat_id'),
                "parse_mode": parse_mode,
                "text": data.get('content')
            },
            timeout=2
        )
        return response


def api_call(method_name, parse_mode, **kwargs):
    client = TelegramBotClient()
    return client.api_call(method_name, parse_mode, **kwargs)
