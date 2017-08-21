from chalice import Chalice, Rate
import json
from chalicelib.telegrambot.processing import BotProcessing
from chalicelib.telegrambot.commands import BotCommands
from chalicelib.telegrambot.utils import send_html_message

app = Chalice(app_name='advaerbot')
app.debug = True


@app.route('/advaerbot', methods=['POST'], content_types=['application/json'])
def index():
    processing = BotProcessing()
    data = app.current_request.json_body
    app.log.debug(json.dumps(data))
    response = processing.process(data)
    return response


@app.schedule(Rate(45, unit=Rate.MINUTES))
def inform(event):
    commands = BotCommands()
    content = "AUTO INFORM\n{}".format(commands.get_ticker(market='btcuah'))
    chat_id = 371271568
    send_html_message(chat_id=chat_id, content=content)
