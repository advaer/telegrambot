TELEGRAM_BOT_TOKEN = ''

try:
    from chalicelib.conf.secret import *
except ImportError:
    print('chalicelib.config.secret cannot be imported!')
