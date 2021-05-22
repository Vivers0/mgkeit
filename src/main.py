import asyncio, requests, settings
from telebot import TeleBot, types
from threading import (Event, Thread)

bot = TeleBot(settings.TOKEN)

from keybutton import Keybutton
from database import Database
from notify import Notify
from send import Send
from timetable import Timetable
database = Database(bot)
keybutton = Keybutton(bot)
send = Send(bot)
notify = Notify(bot)
timetable = Timetable(bot)

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
            timetable.today_timetable(message)
        elif msg == '👨🏻‍🎓 Расписание на завтра':
            timetable.tomorrow_timetable(message)
        elif msg == '🔔 Уведомления':
            database.notify(message)
        else:
            timetable.another_day_timetable(message)
    
def timer_timetable():
    asyncio.run(notify.notify_main())

def main():
    bot.polling()

if __name__ == '__main__':
    print('Ready!')
    p1 = Thread(target=timer_timetable)
    p2 = Thread(target=main)
    p1.start()
    p2.start()
