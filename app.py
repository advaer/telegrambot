import json
from datetime import datetime

import requests
from chalice import Chalice, Rate

from chalicelib.conf import settings
from chalicelib.db.models import CurrencyRate, session
from chalicelib.telegrambot.processing import BotProcessing

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
def get_currency_rate(event):
    api_url = 'http://www.apilayer.net/api/live?access_key={}&currencies=UAH,USD,EUR'.format(
        settings.CURRENCY_ACCESS_KEY,
    )
    r = requests.get(api_url)
    dt = r.json()['timestamp']
    created_at = datetime.fromtimestamp(dt)
    USDUAH = r.json()['quotes'][f'USDUAH']
    USDEUR = r.json()['quotes'][f'USDEUR']
    EURUAH = USDUAH/USDEUR
    session.add_all([
        CurrencyRate(
            base_currency='USD',
            counter_currency='UAH',
            rate=USDUAH,
            created_at=created_at
        ),
        CurrencyRate(
            base_currency='EUR',
            counter_currency='UAH',
            rate=EURUAH,
            created_at=created_at
        )
    ])
    session.commit()
