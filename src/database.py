import requests, asyncio, schedule
from datetime import datetime
from collections import Counter
from course import get_course_id as course
from errorHandler import errorHandler as error
from keybutton import Keybutton


class Database:
    def __init__(self, bot):
        self.bot = bot;
        self.keybutton = Keybutton(self.bot)
        self.user = "http://vivers0.pythonanywhere.com/api/user/"
        # self.timetable = "http://vivers0.pythonanywhere.com/api/timetable/"
        self.timetable = "http://localhost:8000/api/timetable/"
        # Time
        self.eval = ['Четная', 'Нечетная']
        self.week = ['Понедельник', 'Вторник', 'Среду', 'Четверг', 'Пятницу', 'Субботу', 'Воскресенье']

    def registration(self, message):
        def check_user_in_db(user_id):
            try:
                r = requests.get(self.user+str(user_id))
            except requests.RequestException:
                pass 
            return True if r.status_code == 404 else False

        user_id = message.from_user.id
        if check_user_in_db(user_id) == False:
            try:
                r = requests.post(self.user, json={"user": {"user_id": user_id, "course_id": 0, "notify": False }}, headers={"Content-Type": "application/json"})
            except requests.RequestException:
                pass 
            if r.status_code == 200:
                self.bot.send_message(message.chat.id, 'Отлично! Для начала укажи, на каком курсе ты учишься 😜')
                self.bot.register_next_step_handler(message, self.set_course)
            else:
                error(self.bot, message, 'except')
        else:
            self.bot.reply_to(message, 'Ты уже есть в базе данных 😊')

    def set_course(self, message):
        user_id = message.from_user.id
        course_id = course(message.text)
        if course_id == 0:
            msg = self.bot.send_message(user_id, 'Я не нашел такого курса 🙁. Попробуй еще раз:)')
            self.bot.register_next_step_handler(msg, self.set_course)
        else:
            try:
                r = requests.put(self.user+str(user_id), json={"course_id": course_id}, headers={"Content-Type": "application/json"})
            except requests.RequestException:
                pass
            if r.status_code == 200:
                self.bot.send_message(user_id, 'Отлично! Если ты хочешь получать уведомления с расписанием каждый день в 7 утра, то просто напиши /notify или нажми на этот текст:)')
                self.keybutton.send_menu(message)
            else:
                self.bot.send_message(user_id, 'Что-то пошло не так, попробуй еще раз зарегистрироваться - /reset')
        
    def notify(self, message):
        user_id = message.from_user.id
        try:
            r = requests.get(self.user+str(user_id), headers={"Content-Type": "application/json"})
        except requests.RequestException:
            pass
        if r.status_code == 200:
            if r.json()['user']['notify'] == False:
                try:
                    res = requests.put(self.user+str(user_id), json={ 'notify': True }, headers={ "Content-Type": "application/json" })
                except requests.RequestException:
                    pass
                if res.status_code == 200:
                    self.bot.send_message(user_id, 'Автоматическая отправка расписания: *Включено*')
            else:
                try:
                    res = requests.put(self.user+str(user_id), json={ 'notify': False }, headers={"Content-Type": "application/json"})
                except requests.RequestException:
                    pass
                if res.status_code == 200:
                    self.bot.send_message(user_id, 'Автоматическая отправка расписания: *Выключено*')
        else:
            self.bot.send_message(user_id, 'Что-то пошло не так, попробуй еще раз зарегистрироваться - /reset')

    def reset(self, message):
        user_id = message.from_user.id
        try:
            r = requests.delete(self.user+str(user_id))
        except requests.RequestException:
            pass
        if r.status_code == 200:
            self.bot.send_message(user_id, 'Я удалил всю информацию о тебе. Теперь тебе нужно заново зарегистрироваться - /start')
        else:
            self.bot.send_message(user_id, 'Что-то пошло не так, попробуй еще раз зарегистрироваться - /reset')

    # Method

    def get_user_course(self, message):
        r = requests.get(self.user+str(message.from_user.id))
        if r.status_code == 200:
            return r.json()['user']['course_id']
    # Responce

    def get(self, typeу):
        try:
            return requests.get(typeу).json()
        except requests.RequestException:
            print("Database: RequestException")

        