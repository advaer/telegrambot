EXPRESSIONS = {
    '>': {
        'html': '&gt;',
        'result': [1]
    },
    '<': {
        'html': '&lt;',
        'result': [-1]
    },
    '=': {
        'html': '=',
        'result': [-1]
    },
    '>=': {
        'html': '&gt;=',
        'result': [1, 0]
    },
    '<=': {
        'html': '&lt;=',
        'result': [-1, 0]
    }
}

MAIN_MENU = """
<b>POLONIEX tickers:</b>
/btcusd - BTC/USD ticker
/btceur - BTC/EUR ticker
/btcuah - BTC/UAH ticker

/ethusd - ETH/USD ticker
/etheur - ETH/EUR ticker
/ethuah - ETH/UAH ticker

/ltcusd - LTC/USD ticker
/ltceur - LTC/EUR ticker
/ltcuah - LTC/UAH ticker

/bchusd - BCH/USD ticker
/bcheur - BCH/EUR ticker
/bchuah - BCH/UAH ticker

/xmrusd - XMR/USD ticker
/xmreur - XMR/EUR ticker
/xmruah - XMR/UAH ticker

<b>ALERTS. Let me keep you on track:</b>
/alerts - list all active alerts with ID
/stopalert ID - stop alert by ID
/setalert btc eur &gt; 3705.67 - set new alert

<b>Need a Moment?</b>
/chuck - relax from crypto currency
and get new fact about Chuck Norris :)"""
