from telebot import TeleBot, types
from database import DB
from timer import Timer
from threading import (Event, Thread)
from keybutton import Keybutton
import asyncio, requests
from settings import *


bot = TeleBot(TOKEN)
database = DB(bot)
timer = Timer()
keybutton = Keybutton(bot)

# Commands

@bot.message_handler(commands=['start'])
def send_welcome(message):
    database.registration(message)

@bot.message_handler(content_types=['text'])
def handler_for_button(message):
    if message.chat.type == 'private':
        msg = message.text
        if msg == '🔔 Уведомления':
            database.notify(message)

@bot.message_handler(commands=['reset'])
def reset_command(message):
    database.reset(message)
    
def main():
    bot.polling()

if __name__ == '__main__':
    print('Ready!')
    main() 
