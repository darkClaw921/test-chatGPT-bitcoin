import os
import random
import telebot
from datetime import datetime
from dotenv import load_dotenv
from pprint import pprint
from chat import GPT
from datetime import datetime
import workYDB2
from createKeyboard import create_menu_keyboard

load_dotenv()

gpt = GPT()
GPT.set_key(os.getenv('KEY_AI2'))
bot = telebot.TeleBot(os.getenv('TELEBOT_TOKEN2'))
# инициализация бота и диспетчера
#dp = Dispatcher(bot)
sql = workYDB2.Ydb()

# model_index=gpt.load_search_indexes('https://docs.google.com/document/d/1nMjBCoI3WpWofpVRI0rsi-iHjVSeC358JDwN96UW/edit?usp=sharing')
#model_index=sql.select_query('model', 'model=main')


def time_epoch():
    from time import mktime
    dt = datetime.now()
    sec_since_epoch = mktime(dt.timetuple()) + dt.microsecond/1000000.0

    millis_since_epoch = sec_since_epoch * 1000
    return int(millis_since_epoch)


def get_model_url(modelName: str):
    modelUrl = sql.select_query('model', f'model = "{modelName}"')[0]['url']
    print('a', modelUrl)
    return modelUrl.decode('utf-8')


@bot.message_handler(commands=['addmodel'])
def add_new_model(message):
    sql.set_payload(message.chat.id, 'addmodel')
    bot.send_message(message.chat.id,
                     "Пришлите ссылку на google document и через пробел название модели (model1). Не используйте уже существующие названия модели\n Внимани! конец ссылки должен вылядить так /edit?usp=sharing\nи подождите 20сек",)


@bot.message_handler(commands=['addpromt'])
def add_new_promt(message):
    sql.set_payload(message.chat.id, 'addpromt')
    bot.send_message(message.chat.id,
                     "Пришлите ссылку на google document и через пробел название промта (promt1). Не используйте уже существующие названия промта\n Внимани! конец ссылки должен вылядить так /edit?usp=sharing",)


@bot.message_handler(commands=['help', 'start'])
def say_welcome(message):
    row = {'id': 'Uint64', 'MODEL_DIALOG': 'String', 'TEXT': 'String'}
    sql.create_table(str(message.chat.id), row)
    row = {'id': message.chat.id, 'model': '', 'promt': ''}
    sql.replace_query('user', row)

    bot.send_message(message.chat.id, """Привет. Я Chat GPT-4, ИИ-аналитик по BTC""", reply_keyboard=create_menu_keyboard())
#expert_promt = gpt.load_prompt('https://docs.google.com/document/d/181Q-jJpSpV0PGnGnx45zQTHlHSQxXvkpuqlKmVlHDvU/')


@bot.message_handler(commands=['restart'])
def restart_modal_index(message):
    global model_index
    model_index = gpt.load_search_indexes(
        'https://docs.google.com/document/d/1nMjBCoI3WpWofpVRI0rsi-iHjVSeC358JDwN96U/edit?usp=sharing')


@bot.message_handler(commands=['context'])
def send_button(message):
    promt = sql.select_query('user', f"id={message.chat.id}")[
        0]['promt'].decode('utf-8')
    payload = sql.get_payload(message.chat.id)
    #context = sql.get_context(message.chat.id, payload)
    #model = get_model_url(payload)
    #answer = gpt.answer(validation_promt, context, temp = 0.1)
    try:
        sql.delete_query(message.chat.id, f'MODEL_DIALOG = "{payload}"')
        sql.set_payload(message.chat.id, ' ')
    except:
        bot.send_message(message.chat.id,
                         "у вас небыло активного диалога контекст сброшен",)

    #bot.send_message(message.chat.id, answer)
    bot.send_message(message.chat.id,
                     "Контекст сброшен",)


@bot.message_handler(commands=['model1'])
def dialog_model1(message):
    #payload = sql.get_payload(message.chat.id)
    sql.set_payload(message.chat.id, 'model1')
    model = sql.select_query('user', f'id={message.chat.id}')[0]['model']
    promt = sql.select_query('user', f'id={message.chat.id}')[0]['promt']

    bot.send_message(message.chat.id, f'вы работаете по моделе {model}',)
    bot.send_message(message.chat.id, f'вы работаете по промту {promt}',)
    bot.send_message(message.chat.id, 'Что вы хотите узнать?',)


@bot.message_handler(commands=['promt1'])
def work_promt1(message):
    #payload = sql.get_payload(message.chat.id)
    promt = sql.select_query('promt', f'promt="promt1"')[
        0]['url'].decode('utf-8')
    row = {'id': message.chat.id, 'promt': 'promt1'}
    sql.replace_query('user', row)
    sql.set_payload(message.chat.id, 'promt1')
    #promt = sql.select_query('user', f'id={message.chat.id}', row)
    bot.send_message(
        message.chat.id, f'вы работаете по промту {promt}', reply_markup=create_menu_keyboard())


@bot.message_handler(commands=['promt2'])
def work_promt2(message):
    #payload = sql.get_payload(message.chat.id)
    promt = sql.select_query('promt', f'promt="promt2"')[
        0]['url'].decode('utf-8')
    row = {'id': message.chat.id, 'promt': 'promt2'}
    sql.replace_query('user', row)
    sql.set_payload(message.chat.id, 'promt2')
    #promt = sql.select_query('user', f'id={message.chat.id}', row)
    bot.send_message(
        message.chat.id, f'вы работаете по промту {promt}', reply_markup=create_menu_keyboard())


@bot.message_handler(content_types=['text'])
def any_message(message):
    print('это сообщение', message)
    #text = message.text.lower()
    text = message.text
    userID = message.chat.id
    try:
        payload = sql.get_payload(userID)
    except:
        payload = 'a'

    if payload == 'addpromt':
        text = text.split(' ')
        rows = {'promt': text[1], 'url': text[0]}
        # sql.insert_query('model',rows)
        sql.replace_query('promt', rows)
    
    if text == 'Аналитика BTC на 5 дней':
        promptUrl = sql.select_query('promt', 'promt="promt1"')[0]['url'].decode('utf-8')
    if text == 'Аналитика BTC на 15 дней':
        promptUrl = sql.select_query('promt', 'promt="promt2"')[0]['url'].decode('utf-8')
    
    if text == 'Аналитика BTC на 30 дней':
        promptUrl = sql.select_query('promt', 'promt="promt3"')[0]['url'].decode('utf-8')
    
    promt = gpt.load_prompt(promptUrl)
    print(f'{promptUrl=}')
    try:
        answer = gpt.answer(promt, ' ', temp=1)
    except Exception as e:
        bot.send_message(message.chat.id, f'{e}')
        return 0
    
    bot.send_message(message.chat.id, answer)
    return 0
    #context = sql.get_context(userID, payload)
    # if context is None or context == '' or context == []:
    #    context = text

    #print('context2', context + f'клиент: {text}')
    #model= gpt.load_prompt('https://docs.google.com/document/d/1f4GMt2utNHsrSjqwE9tZ7R632_ceSdgK6k-_QwyioZA/edit?usp=sharing')
    # try:
    promt = sql.select_query('user', f'id={message.chat.id}')[
        0]['promt'].decode('utf-8')
    promtUrl = sql.select_query('promt', f'promt="{promt}"')[
        0]['url'].decode('utf-8')
    #    modelUrl = sql.select_query('user', f'id={message.chat.id}')['model']
    #    promt= gpt.load_prompt(get_model_url(promtUrl))
    #    answer = gpt.answer_index(promt, text, modelUrl)
    # except:
    #bot.send_message(message.chat.id, 'У вас не выбран пром, работа по стандартному')
    #promt= 'https://docs.google.com/document/d/1KbXMyyIbf4BKFkZeQfzKyzU8blCKoXmFl9du2UD0I7c/edit?usp=sharing'
    promt = gpt.load_prompt(promtUrl)
    try:
        answer = gpt.answer(promt, text, temp=1)
    except Exception as e:
        bot.send_message(message.chat.id, f'{e}')
        return 0
    #model= gpt.load_prompt(get_model_url(payload))
    #answer = gpt.answer(model, text, temp = 0.1)
    #answer = gpt.answer_index(promt, text, model_index,)
    print('answer', answer)
    bot.send_message(message.chat.id, answer)
    # if payload == 'model3':
    rows = {'id': time_epoch(), 'MODEL_DIALOG': payload,
            'TEXT': f'клиент: {text}'}
    sql.insert_query(userID,  rows)

    rows = {'id': time_epoch()+1, 'MODEL_DIALOG': payload,
            'TEXT': f'менеджер: {answer}'}
    sql.insert_query(userID,  rows)


bot.infinity_polling()
