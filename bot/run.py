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
        # Fetch 1m candles
        ohlcv = exchange.fetch_ohlcv(pair, '1m')
        df1m = pd.DataFrame(ohlcv, columns=['time', 'open', 'high', 'low', 'close', 'volume'])

        # Fetch 1h candles
        ohlcv = exchange.fetch_ohlcv(pair, '1h')
        df1h = pd.DataFrame(ohlcv, columns=['time', 'open', 'high', 'low', 'close', 'volume'])

        # Calculate necessary timeframe
        df4h = recalculate_candlestick(df1h, '4H')
        df15m = recalculate_candlestick(df1m, '15min')
        
        stoch_results = df4h.ta.stoch(k=config.get('K_LENGTH'), d = config.get('D_SMOOTHING'), smooth_k = config.get('K_SMOOTHING'))
        stoch_results15m = df15m.ta.stoch(k=config.get('K_LENGTH'), d = config.get('D_SMOOTHING'), smooth_k = config.get('K_SMOOTHING'))
       
        prev_stoch_k = round(stoch_results.iloc[-2][0], 2)
        prev_stoch_d = round(stoch_results.iloc[-2][1], 2)

        current_stoch_k = round(stoch_results.iloc[-1][0], 2)
        current_stoch_d = round(stoch_results.iloc[-1][1], 2)

        prev_stoch15m_k = round(stoch_results15m.iloc[-2][0], 2)
        prev_stoch15m_d = round(stoch_results15m.iloc[-2][1], 2)

        current_stoch15m_k = round(stoch_results15m.iloc[-1][0], 2)
        current_stoch15m_d = round(stoch_results15m.iloc[-1][1], 2)

        print(f"Check pair {pair}")

        if stoch_cross(prev_stoch_k, prev_stoch_d, current_stoch_k, current_stoch_d, 65) and \
            stoch_cross(prev_stoch15m_k, prev_stoch15m_d, current_stoch15m_k, current_stoch15m_d, 55):
            print(f"Found signal")

            send_signal("USD_" + pair, 9974970)

            send_notification(
                f"Pair: {pair} - stoch 4h prev_k: {prev_stoch_k} prev_d: {prev_stoch_d}  curr_k: {current_stoch_k} curr_d: {current_stoch_d} \
                    15m prev_k: {prev_stoch15m_k} prev_d: {prev_stoch15m_d}  curr_k: {current_stoch15m_k} curr_d: {current_stoch15m_d}")

    send_notification(f"Finish searching")

def stoch_cross(prev_stoch_k, prev_stoch_d, current_stoch_k, current_stoch_d, min_level):
    return (current_stoch_k < current_stoch_d) \
        and (prev_stoch_k > prev_stoch_d) \
        and (current_stoch_d > min_level) \
        and (current_stoch_k > min_level)

def recalculate_candlestick(df, time_frame):
    aggs = {
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
    }

    result_df = df.copy()

    result_df['time'] = pd.to_datetime(result_df['time'], unit='ms')

    return result_df.resample(time_frame, on='time').apply(aggs)
