from chalice import Chalice, Rate
import json
import requests

app = Chalice(app_name='advaerbot')

app.debug = True


TEXT = {
    '/start': "Hi! I am test Telegram bot developed by <b>Rinat Advaer</b>.\n"
              "/help - use it for help.\n"
              "/chuck - get new fact about Chuck Norris.\n"
              "For any other questions, please contact my creator: @advaer",
    '/help': "Not much to do here for now\n"
             "/chuck - get new fact about Chuck Norris.\n"
}


def get_chuck_quote(key):
    quote = requests.get('https://api.chucknorris.io/jokes/random')
    return json.loads(quote.text).get('value')


def get_static_text(key):
    return TEXT[key]

BOT_DATA = {
    '/start': get_static_text,
    '/help': get_static_text,
    '/chuck': get_chuck_quote,
}


@app.route('/advaerbot', methods=['POST'], content_types=['application/json'])
def index():
    data = app.current_request.json_body
    message = data.get("message")
    app.log.debug(json.dumps(data))
    if message:
        r = requests.post(
            'https://api.telegram.org/bot385440215:AAEBzlx5FLSJ6m8aF2CrQtl0NIy7oR1YDqQ/sendMessage',
            data={
                "chat_id": message.get('from').get('id'),
                "parse_mode": "HTML",
                "text": BOT_DATA[message.get('text')](message.get('text'))
            }
        )
    return {'status': 'ok'}

