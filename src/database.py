import requests
from course import get_course_id as course
from errorHandler import errorHandler as error
class DB:
    def __init__(self, bot):
        self.bot = bot
        self.user = "http://vivers0.pythonanywhere.com/api/user/"
        self.timetable = "http://vivers0.pythonanywhere.com/api/timetable/"

    # def today_timetable(self, message):
    #     for i in self.timetable['timetable']:
    #         if i['course_id'] == 31:
    #             self.bot.reply_to(message, i['timetable'])

    def registration(self, message):
        def check_user_in_db(user_id):
            r = requests.get(self.user+str(user_id))
            return True if r.status_code == 404 else False

        user_id = message.from_user.id
        if check_user_in_db(user_id) == False:
            r = requests.post(self.user, json={"user": {"user_id": user_id, "course_id": 0, "notify": False }}, headers={"Content-Type": "application/json"})
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
            r = requests.put(self.user+str(user_id), json={"course_id": course_id}, headers={"Content-Type": "application/json"})
            if r.status_code == 200:
                self.bot.send_message(user_id, 'Отлично! Если ты хочешь получать уведомления с расписанием каждый день в 7 утра, то просто напиши /notify или нажми на этот текст:)')
            else:
                print('61 str')

    def reset(self, message):
        user_id = message.from_user.id
        r = requests.delete(self.user+str(user_id))
        if r.status_code == 200:
            self.bot.send_message(user_id, 'Я удалил всю информацию о тебе. Теперь тебе нужно заново зарегистрироваться - /start')
        else:
            error(self.bot, message, 'except')

    def notify(self, message):
        user_id = message.from_user.id
        r = requests.get(self.user+str(user_id), headers={"Content-Type": "application/json"})
        if r.status_code == 200:
            if r.json()['user']['notify'] == False:
                res = requests.put(self.user+str(user_id), json={ 'notify': True }, headers={ "Content-Type": "application/json" })
                if res.status_code == 200:
                    self.bot.send_message(user_id, 'Автоматическая отправка расписания: *Включено*')
            else:
                res = requests.put(self.user+str(user_id), json={ 'notify': False }, headers={"Content-Type": "application/json"})
                if res.status_code == 200:
                    self.bot.send_message(user_id, 'Автоматическая отправка расписания: *Выключено*')
        else:
            error(self.bot, message, 'except')