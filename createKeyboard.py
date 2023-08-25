import telebot

def create_menu_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    #keyboard.row('/addmodel')
    #keyboard.row('/addpromt')
    #keyboard.row('/context')
    #keyboard.row('/promt1') 
    #keyboard.row('/promt2')
    #keyboard.row('Аналитика BTC на 5 дней')
    keyboard.row('Bitcoin','Ethereum','BNB')
    
    #keyboard.row('Аналитика BTC на 15 дней')
    keyboard.row('Ripple','Cardano','Solana')
    
    #keyboard.row('Аналитика BTC на 30 дней')
    keyboard.row('TRON','Polkadot','Polygon')
    
    #keyboard.row('')
    keyboard.row('Dogecoin')
    return keyboard