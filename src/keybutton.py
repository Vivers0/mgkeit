from telebot import types

class Keybutton:
    def __init__(self, bot):
        self.bot = bot

    def send_build(self, message):
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Корпус на Судостроительной', callback_data='mill')
        button2 = types.InlineKeyboardButton('Корпус на Миллионщикова', callback_data='mill')
        markup.add(button1, button2)
        self.bot.send_message(message.chat.id, 'Отлично! Для начала укажи, в каком корпусе ты учишься 😜', reply_markup=markup)
        
    def send_menu(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton('✍🏻 Расписание на сегодня')
        btn2 = types.KeyboardButton('👨🏻‍🎓 Расписание на завтра')
        btn3 = types.KeyboardButton('🔔 Уведомления')
        markup.add(btn1, btn2, btn3)
        self.bot.send_message(message.chat.id, 'Вот список комманд. Если хочешь посмотреть расписание на другой день, то просто напиши, какой день недели тебе нужен (Например: Втроник или Пятница)', reply_markup=markup)  
