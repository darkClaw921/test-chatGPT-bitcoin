from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from pprint import pprint
from dotenv import load_dotenv
import os 
from dataclasses import dataclass
from datetime import datetime
from typing import List
load_dotenv()
api_key = os.environ.get('api_key_binance')
api_secret = os.environ.get('api_secret_binance')

client = Client(api_key, api_secret)

@dataclass
class BTC_history:
    dateOpen:int = 0
    dateClose:int =6 

def candle_data_to_dict(candle_data: List[str]) -> dict:
    keys = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
            'Close time', 'Quote asset volume', 'Number of trades',
            'Taker buy base asset volume', 'Taker buy quote asset volume',
            'Ignore']
    
    #for i in range(len(keys)):

    return {keys[i]: candle_data[i] for i in range(len(keys))}
def timeEpoh(time: int)->str:
    pass

def timestamp_to_date(timestamp):
    dt_object = datetime.fromtimestamp(int(timestamp)/1000)
    #print(dt_object)
    return dt_object.strftime("%d/%m/%y")

def prepare_list(lst:list)->list:
    text = ''
    for i in lst:
        i[0] = timestamp_to_date(i[BTC_history.dateOpen])
        i[6] = timestamp_to_date(i[BTC_history.dateClose])
        candle_dict = candle_data_to_dict(i)
        #print(candle_dict)
        text += f"\n& {candle_dict['Open time']}; {round(float(candle_dict['High']))}; {round(float(candle_dict['Low']))}; {round(float(candle_dict['Close']))}; {round(float(candle_dict['Volume']))}; {candle_dict['Close time']}; {round(float(candle_dict['Quote asset volume']))}; {round(float(candle_dict['Number of trades']))}"
        #print(text)
        #print(i[BTC_history.date])
        #row = f'{date}'
        #print(row)
    return text
    pass


def get_BTC_analit_for(dayStart:str )-> str:
    """_summary_

    Args:
        dayStart (str): 'на 5 дней'

    Returns:
        str: _description_
    """
    setting={'Аналитика BTC на 5 дней':[Client.KLINE_INTERVAL_1DAY, '3 month ago UTC'],
            'Аналитика BTC на 15 дней':[Client.KLINE_INTERVAL_1DAY , '3 month ago UTC'],
            'Аналитика BTC на 30 дней':[Client.KLINE_INTERVAL_1WEEK, '2 year ago UTC'],}

    setting =setting[dayStart]
    #klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1WEEK, start_day)
    klines = client.get_historical_klines("BTCUSDT", setting[0], setting[1])
    #pprint(klines)
    #print(len(klines))
    history = prepare_list(klines)
    return history

if __name__ == '__main__':
    #b =datetime.fromtimestamp(1685318400000/1000).strftime('%c')
    #print(b)
    #a = 1656288000000
    #timestamp_to_date(a/1000)
    btc = get_BTC_analit_for('на 5 дней')
    print(btc)

