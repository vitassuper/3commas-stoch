from bot.commas import send_signal
from bot.configurator import load_config
from bot.connector import connect
import pandas as pd
import pandas_ta as ta
from bot.markets import get_markets
from bot.notificator import send_notification
import schedule
import time

def run():
    schedule.every(3).minutes.do(get_signal)

    while True:
        schedule.run_pending()
        time.sleep(1)


def get_signal():
    config = load_config()
    exchange = connect()

    config = config.get('STOCH')

    send_notification(f"Start searching")

    for pair in get_markets():
        ohlcv = exchange.fetch_ohlcv(pair, '4h')
        ohlcv2 = exchange.fetch_ohlcv(pair, '15m')

        df = pd.DataFrame(ohlcv, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        df2 = pd.DataFrame(ohlcv2, columns=['time', 'open', 'high', 'low', 'close', 'volume'])

        stoch_results = df.ta.stoch(k=config.get('K_LENGTH'), d = config.get('D_SMOOTHING'), smooth_k = config.get('K_SMOOTHING'))
        stoch_results15m = df2.ta.stoch(k=config.get('K_LENGTH'), d = config.get('D_SMOOTHING'), smooth_k = config.get('K_SMOOTHING'))

        prev_stock_k = round(stoch_results.iloc[-2][0], 2)
        prev_stock_d = round(stoch_results.iloc[-2][1], 2)

        current_stock_k = round(stoch_results.iloc[-1][0], 2)
        current_stock_d = round(stoch_results.iloc[-1][1], 2)


        prev_stock15m_k = round(stoch_results15m.iloc[-2][0], 2)
        prev_stock15m_d = round(stoch_results15m.iloc[-2][1], 2)

        current_stock15m_k = round(stoch_results15m.iloc[-1][0], 2)
        current_stock15m_d = round(stoch_results15m.iloc[-1][1], 2)

        # if (current_stock15m_k < current_stock15m_d) and (prev_stock15m_k > prev_stock15m_d) and (current_stock15m_d > 80):
        #     print(f"Found signal")

        #     send_signal("USD_" + pair, 9984618)

        #     send_notification(
        #         f"Pair: {pair} - stoch signal prev k: {prev_stock15m_k} prev d: {prev_stock15m_d}  current k: {current_stock15m_k} current d: {current_stock15m_d}")

        if (current_stock_k < current_stock_d) and (prev_stock_k > prev_stock_d) and (current_stock_d > 75) and (current_stock15m_k > 55):
            print(f"Found signal")

            send_signal("USD_" + pair, 9974970)

            send_notification(
                f"Pair: {pair} - stoch signal prev k: {prev_stock_k} prev d: {prev_stock_d}  current k: {current_stock_k} current d: {current_stock_d}")

    send_notification(f"Finish iteration")
