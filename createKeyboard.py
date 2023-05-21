import telebot

def create_menu_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    #keyboard.row('/addmodel')
    keyboard.row('/addpromt')
    keyboard.row('/context')
    keyboard.row('/promt1') 
    keyboard.row('/promt2')
    return keyboard