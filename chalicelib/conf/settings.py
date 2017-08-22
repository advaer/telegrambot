TELEGRAM_BOT_TOKEN = ''
DATABASE_URL = ''
CURRENCY_ACCESS_KEY = ''
try:
    from chalicelib.conf.secret import *
except ImportError:
    print('chalicelib.config.secret cannot be imported!')
