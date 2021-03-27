import requests
from course import Course
from errorHandler import errorHandler as error
class DB:
    def __init__(self, bot):
        self.bot = bot
        self.link = {"timetable": "http://127.0.0.1:8000/api/timetable/", "person": "http://127.0.0.1:8000/api/user/"}

    # def today_timetable(self, message):
    #     for i in self.timetable['timetable']:
    #         if i['course_id'] == 31:
    #             self.bot.reply_to(message, i['timetable'])

    def registration(self, message):
        def check_user_in_db(user_id):
            r = requests.get(self.link['person']+str(user_id))
            if r.status_code == 404:
                return False
            else:
                return True

        user_id = message.from_user.id
        if check_user_in_db(user_id) == False:
            r = requests.post(self.link['person'], json={"user": {"user_id": user_id, "course_id": 0, "notify": False }}, headers={"Content-Type": "application/json"})
            if r.status_code == 200:
                self.bot.send_message(message.chat.id, 'Отлично! Для начала укажи, на каком курсе ты учишься 😜')
                self.bot.register_next_step_handler(message, self.set_course)
        else:
            self.bot.reply_to(message, 'Ты уже есть в базе данных 😊')

    def set_course(self, message):
        text = message.text
        user_id = message.from_user.id
        # course_id = course.get_course_id(text)
        course_id = 1
        if course_id == 0:
            mes = self.bot.send_message(user_id, 'Я не нашел такого курса 🙁. Попробуй еще раз:)')
            self.bot.register_next_step_handler(mes, self.set_course)
        else:
            r = requests.put('http://127.0.0.1:8000/api/user/{}'.format(user_id), json={"course_id": course_id}, headers={"Content-Type": "application/json"})
            if r.status_code == 200:
                self.bot.send_message(user_id, 'Отлично! Если ты хочешь получать уведомления с расписанием каждый день в 7 утра, то просто напиши /notify или нажми на этот текст:)')
            else:
                print('61 str')

    def reset(self, message):
        user_id = message.from_user.id
        r = requests.delete('http://127.0.0.1:8000/api/user/{}'.format(user_id))
        if r.status_code == 200:
            self.bot.send_message(user_id, 'Я удалил всю информацию о тебе. Теперь тебе нужно заново зарегистрироваться - /start')

    def notify(self, message):
        user_id = message.from_user.id
        r = requests.get('http://127.0.0.1:8000/api/user/{}'.format(user_id))
        if r.status_code == 200:
            if r.json()['user']['notify'] == False:
                res = requests.put('http://127.0.0.1:8000/api/user/{}'.format(user_id), json={ 'notify': True }, headers={ "Content-Type": "application/json" })
                if res.status_code == 200:
                    self.bot.send_message(user_id, 'Автоматическая отправка расписания: *Включено*')
            else:
                res = requests.put('http://127.0.0.1:8000/api/user/{}'.format(user_id), json={ 'notify': False }, headers={"Content-Type": "application/json"})
                if res.status_code == 200:
                    self.bot.send_message(user_id, 'Автоматическая отправка расписания: *Выключено*')