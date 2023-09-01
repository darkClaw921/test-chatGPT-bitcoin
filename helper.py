from datetime import datetime, timedelta
#import workYDB
import redis
import json
#sql = workYDB.Ydb()

#datetime
def time_epoch():
    from time import mktime
    dt = datetime.now()
    sec_since_epoch = mktime(dt.timetuple()) + dt.microsecond/1000000.0

    millis_since_epoch = sec_since_epoch * 1000
    return int(millis_since_epoch)

def get_dates(day):
    # Текущая дата
    current_date = datetime.now().strftime("%d/%m/%Y")

    # Дата, отстоящая на 30 дней
    delta = timedelta(days=day)
    future_date = (datetime.now() + delta).strftime("%d/%m/%Y")

    return current_date, future_date

def date_now():
    #patern = '%Y-%m-%dT%H:%M:%S'
    patern = '%Y-%m-%dT%H:00:00'
    #patern = '%Y-%m-%dT%H'
    current_date = datetime.now().strftime(patern)
    return current_date+'Z'
#YDB
def get_model_url(modelName: str):
    modelUrl = sql.select_query('model', f'model = "{modelName}"')[0]['url']
    print('a', modelUrl)
    return modelUrl.decode('utf-8')

def add_message_to_history(userID:str, role:str, message:str):
    mess = {'role': role, 'content': message}
    r.lpush(userID, json.dumps(mess))

def get_history(userID:str):
    items = r.lrange(userID, 0, -1)
    history = [json.loads(m.decode("utf-8")) for m in items[::-1]]
    return history

def clear_history(userID:str):
    r.delete(userID)

# any
def split_string(string):
    # Размер строки
    length = len(string)
    
    # Индекс середины строки
    middle_index = length // 2
    
    # Разбиение строки на две части
    first_half = string[:middle_index]
    second_half = string[middle_index:]
    
    return first_half, second_half

def sum_dict_values(dict1, dict2):

    result = {}

    for key in dict1:
        if key in dict2:
            result[key] = dict1[key] + dict2[key]
        else:
            result[key] = dict1[key]

    for key in dict2:
        if key not in dict1:
            result[key] = dict2[key]

    return result

coins = {'Bitcoin':'BTCUSDT', 
    'Ethereum':'ETHUSDT',
    'Bnb':'BNBUSDT',
    'Ripple':'XRPUSDT',
    'Cardano':'ADAUSDT',
    'Dogecoin':'DOGEUSDT',
    'Solana':'SOLUSDT',
    'Tron':'TRXUSDT',
    'Polkadot':'DOTUSDT',
    'Polygon':'MATICUSDT'}