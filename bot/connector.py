import ccxt

def connect():
    config = {
        'enableRateLimit': True,
    }

    exchange = ccxt.ftx(config)

    return exchange
