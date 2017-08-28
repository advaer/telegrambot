import json

from chalice import Chalice, Rate

from chalicelib.telegrambot.processing import BotProcessing
from chalicelib.telegrambot.tasks import get_currencies, get_tickers

app = Chalice(app_name='advaerbot')
app.debug = True


@app.route('/advaerbot', methods=['POST'], content_types=['application/json'])
def index():
    processing = BotProcessing()
    data = app.current_request.json_body
    app.log.debug(json.dumps(data))
    response = processing.process(data)
    return response


@app.schedule(Rate(1, unit=Rate.HOURS))
def get_currencies_rate(event):
    get_currencies()


@app.schedule(Rate(10, unit=Rate.MINUTES))
def get_tickers_info(event):
    get_tickers()
