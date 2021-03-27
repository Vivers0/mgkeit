from telebot import TeleBot, types
from database import DB
from timer import Timer
from threading import (Event, Thread)
from keybutton import Keybutton
import asyncio, requests

TOKEN = '935313555:AAHav1AR2uyX-2odJek2pXtmdAN9caCSvew'
bot = TeleBot(TOKEN)
database = DB(bot)
timer = Timer()
keybutton = Keybutton(bot)

# Commands

@bot.message_handler(commands=['start'])
def send_welcome(message):
    database.registration(message)


# @bot.callback_query_handler(func=lambda call: True)
# def callback_build_button(call):
#     database.added_user_build_id(call)

# @bot.message_handler(commands=['menu'])
# def send_menu(message):
#     keybutton.send_menu(message)

# @bot.message_handler(commands=['reset'])
# def reset_command(message):
#     database.reset_user_in_db(message)

# @bot.message_handler(commands=['notify'])
# def notify_command(message):
#     database.enable_notify(message)

# @bot.message_handler(content_types=['text'])
# def handler_for_button(message):
#     if message.chat.type == 'private':
#         msg = message.text
#         if msg == '✍🏻 Расписание на сегодня':
#             database.today_timetable(message)

        # elif msg == '👨🏻‍🎓 Расписание на завтра':
        #     database.get_timetable_button_day(message, 'tomorrow')
        # elif msg == '🔔 Уведомления':
        #     database.enable_notify(message)
        # else:
        #     database.another_day_timetable(message)
    
# def timer_timetable():
    # asyncio.run(database.main_notify())
    
def main():
    bot.polling()

if __name__ == '__main__':
    main()
    print('Ready!') 
    # p1 = Thread(target=timer_timetable)
    # p2 = Thread(target=main)
    # p1.start()
    # p2.start()
