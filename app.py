from chalice import Chalice
import json
from chalicelib.advaerbot.processing import BotProcessing

app = Chalice(app_name='advaerbot')
app.debug = True


@app.route('/advaerbot', methods=['POST'], content_types=['application/json'])
def index():
    processing = BotProcessing()
    data = app.current_request.json_body
    app.log.debug(json.dumps(data))
    return processing.process(data)
