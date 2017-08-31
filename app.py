import json
from chalicelib.db.models import session
from chalice import (
    Chalice,
    Rate,
)

from chalicelib.telegrambot.processing import BotProcessing
from chalicelib.telegrambot.tasks import (
    get_currencies,
    get_tickers,
    process_all_alerts,
)

app = Chalice(app_name='advaerbot')
app.debug = True


@app.route('/advaerbot', methods=['POST'], content_types=['application/json'])
def index():
    app.log.debug("START index")
    processing = BotProcessing()
    data = app.current_request.json_body
    app.log.debug(json.dumps(data))
    response = processing.process(data)
    session.close()
    return response


@app.schedule(Rate(1, unit=Rate.HOURS))
def get_currencies_rate(event):
    app.log.debug("START get_currencies_rate")
    get_currencies()
    session.close()


@app.schedule(Rate(10, unit=Rate.MINUTES))
def get_tickers_info(event):
    app.log.debug("START get_ticker_info")
    get_tickers()
    session.close()


@app.schedule(Rate(1, unit=Rate.MINUTES))
def send_alerts(event):
    app.log.debug("START send_alerts")
    process_all_alerts()
    session.close()
