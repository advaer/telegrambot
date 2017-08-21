from .client import api_call


def send_html_message(**kwargs):
    return api_call('sendMessage', parse_mode='HTML', **kwargs)
