from telebot import TeleBot, types
from database import DB
from threading import (Event, Thread)
from keybutton import Keybutton
import asyncio, requests
from settings import *


bot = TeleBot(TOKEN)
database = DB(bot)
keybutton = Keybutton(bot)

# Commands

@bot.message_handler(commands=['start'])
def send_welcome(message):
    database.registration(message)

@bot.message_handler(commands=['reset'])
def reset_command(message):
    database.reset(message)

@bot.message_handler(commands=['menu'])
def send_menu(message):
    keybutton.send_menu(message)

@bot.message_handler(commands=['notify'])
def send_notify(message):
    database.notify(message)

@bot.message_handler(content_types=['text'])
def handler_for_button(message):
    if message.chat.type == 'private':
        msg = message.text
        if msg == '✍🏻 Расписание на сегодня':
            database.today_timetable(message)
        elif msg == '👨🏻‍🎓 Расписание на завтра':
            database.get_timetable_button_day(message, 'tomorrow')
        elif msg == '🔔 Уведомления':
            database.notify(message)
        else:
            database.another_day_timetable(message)
    
def timer_timetable():
    asyncio.run(database.main_notify())

def main():
    bot.polling()

if __name__ == '__main__':
    print('Ready!')
    p1 = Thread(target=timer_timetable)
    p2 = Thread(target=main)
    p1.start()
    p2.start()
