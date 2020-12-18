from telebot import TeleBot, types
from database import DB
from timer import Timer
from threading import (Event, Thread)
import asyncio

TOKEN = '931991068:AAFd_FJCo2O__5D3l21ZIQiboOaiMU6-1DE'
bot = TeleBot(TOKEN)
database = DB(bot=bot)
timer = Timer(bot)

# Commands

       

@bot.message_handler(commands=['start'])
def send_welcome(message):
    database.added_user_in_db(message)
# res = database.added_user_in_db(message)
# # timer_timetable()
# if res == True:
#     send_build_button(message)

# def send_build_button(message):
#     markup = types.InlineKeyboardMarkup()
#     button1 = types.InlineKeyboardButton('Корпус на Судостроительной', callback_data='mill')
#     button2 = types.InlineKeyboardButton('Корпус на Миллионщикова', callback_data='mill')
#     markup.add(button1, button2)
#     bot.send_message(message.chat.id, 'Отлично! Для начала укажи, в каком корпусе ты учишься 😜', reply_markup=markup)
    

@bot.callback_query_handler(func=lambda call: True)
def callback_build_button(call):
    database.added_user_build_id(call)
# send_course(call.message)
# bot.answer_callback_query(callback_query_id=call.message.chat.id, show_alert=False)
        


@bot.message_handler(commands=['menu'])
def send_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('✍🏻 Расписание на сегодня')
    btn2 = types.KeyboardButton('👨🏻‍🎓 Расписание на завтра')
    btn3 = types.KeyboardButton('🔔 Уведомления')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, 'Вот список комманд. Если хочешь посмотреть расписание на другой день, то просто напиши, какой день недели тебе нужен (Например: Втроник или Пятница)', reply_markup=markup)  

@bot.message_handler(commands=['reset'])
def reset_command(message):
    database.reset_user_in_db(message)

# @bot.message_handler(commands=['notify'])
# def notify_command(message):
    

@bot.message_handler(content_types=['text'])
def handler_for_button(message):
    if message.chat.type == 'private':
        msg = message.text
        if msg == '✍🏻 Расписание на сегодня':
            database.get_timetable_another_day(message, 'today')
        elif msg == '👨🏻‍🎓 Расписание на завтра':
            database.get_timetable_another_day(message, 'tomorrow')
        elif msg == '🔔 Уведомления':
            database.enable_notify(message)
    
def timer_timetable():
    obj = database.check_user_for_notify()
    asyncio.run(timer.sending_messages_with_timetable(obj))
    
def main():
    bot.polling()

if __name__ == '__main__':
    print('Ready!') 
    p1 = Thread(target=timer_timetable)
    p2 = Thread(target=main)
    p1.start()
    p2.start()
