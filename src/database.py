import requests, asyncio, schedule
from datetime import datetime
from collections import Counter
from course import get_course_id as course
from errorHandler import errorHandler as error
class DB:
    def __init__(self, bot):
        self.bot = bot
        self.send = Send(self.bot)
        self.user = "http://vivers0.pythonanywhere.com/api/user/"
        self.timetable = "http://vivers0.pythonanywhere.com/api/timetable/"
        # Time
        self.eval = ['Четная', 'Нечетная']
        self.week = ['Понедельник', 'Вторник', 'Среду', 'Четверг', 'Пятницу', 'Субботу', 'Воскресенье']

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

    def reset(self, message):
        user_id = message.from_user.id
        r = requests.delete(self.user+str(user_id))
        if r.status_code == 200:
            self.bot.send_message(user_id, 'Я удалил всю информацию о тебе. Теперь тебе нужно заново зарегистрироваться - /start')
        else:
            error(self.bot, message, 'except')


    ################
    #
    # Timetable
    #
    ################

    async def main_notify(self):
        def get_user_obj():
            user = dict()
            def timetable(course):
                def is_eval():
                    return 'yes' if int(datetime.today().strftime("%V")) % 2 == 0 else 'no'
                timetable = requests.get('http://vivers0.pythonanywhere.com/api/timetable/').json()
                for i in timetable['timetable']:
                    if i['course_id'] == course:
                        if i['day_week'] == datetime.today().weekday():
                            if i['is_odd'] == is_eval():
                                return i['timetable']

            def users():
                arr = []
                users = requests.get('http://vivers0.pythonanywhere.com/api/user/').json()
                for user in users['users']:
                    if user['notify'] == True:
                        arr.append(user)
                    return arr
            for t in users():
                user[t['user_id']] = dict(timetable=timetable(t['course_id']), day=datetime.today().weekday())
            return user

        def send_message():
            obj = get_user_obj()
            for user in obj:
                timetable = obj[user]['timetable']
                day = self.week[int(obj[id]['day'])]
                self.bot.send_message(user, 'Доброе утро, твое расписание на ' + day + '\n\n' + timetable)
            try:
                self.main_notify()
            except RuntimeWarning:
                print('database: RuntimeWarning')
        schedule.every().day.at('17:17').do(send_message)
        while True:
            schedule.run_pending()
            await asyncio.sleep(1)
                        
    def get_timetable_button_day(self, message, day):
        user_id = message.from_user.id
        if day == 'today':
            self.send.today_button(user_id)
        elif day == 'tomorrow':
            self.send.tomorrow_button(user_id)

    def today_timetable(self, message):
        def timetable(course, day, evall):
            timetable = requests.get('http://vivers0.pythonanywhere.com/api/timetable/').json()
            for i in timetable['timetable']:
                if i['course_id'] == course:
                    if i['day_week'] == day:
                        if i['is_odd'] == evall:
                            return i['timetable']

        def user():
            r = requests.get('http://vivers0.pythonanywhere.com/api/user/'+str(message.from_user.id))
            if r.status_code == 200:
                return r.json()['user']['course_id']

        week = self.week[int(self.send.today_of_week())]
        evals = self.eval[int(self.send.is_eval()['num'])]
        timetable = timetable(user(), self.send.today_of_week(), self.send.is_eval()['word'])
        self.bot.send_message(message.from_user.id, 'Расписание на ' + week + ' ('+ evals +')\n\n' + timetable)

    def another_day_timetable(self, message):
        msg = Counter(str(message.text).upper())
        user_id = message.from_user.id
        if msg == Counter('ПОНЕДЕЛЬНИК'):
            return self.send.another_day(user_id, 0)
        elif msg == Counter('ВТОРНИК'):
            return self.send.another_day(user_id, 1)
        elif msg == Counter('СРЕДА'):
            return self.send.another_day(user_id, 2)
        elif msg == Counter('ЧЕТВЕРГ'):
            return self.send.another_day(user_id, 3)
        elif msg == Counter('ПЯТНИЦА'):
            return self.send.another_day(user_id, 4)
        elif msg == Counter('СУББОТА'):
            return self.send.another_day(user_id, 5)
        elif msg == Counter('ВОСКРЕСЕНЬЕ'):
            return self.send.another_day(user_id, 6)
        else:
            pass

class Send:
    def __init__(self, bot):
        self.bot = bot
        self.eval = ['Четная', 'Нечетная']
        self.week = ['Понедельник', 'Вторник', 'Среду', 'Четверг', 'Пятницу', 'Субботу', 'Воскресенье']

    def today_button(self, id):
        try:
            week = self.week[int(self.today_of_week())]
            evals = self.eval[int(self.is_eval()['num'])]
            timetable = self.get_user_timetable(self.get_user_course(id), self.today_of_week(), self.is_eval()['word'])
            self.bot.send_message(id, 'Расписание на ' + week + ' ('+ evals +')\n\n' + timetable)
        except:
            self.bot.send_message(id, 'Что-то пошло не так, попробуй еще раз зарегистрироваться - /start')

    def tomorrow_button(self, id):
        try:
            week = self.week[int(self.today_of_week())+1]
            evals = self.eval[int(self.is_eval()['num'])]
            timetable = self.get_user_timetable(self.get_user_course(id), self.today_of_week()+1, self.is_eval()['word'])
            self.bot.send_message(id, 'Расписание на ' + week + ' ('+ evals +')\n\n' + timetable)
        except:
            self.bot.send_message(id, 'Что-то пошло не так, попробуй еще раз зарегистрироваться - /start')

    def another_day(self, id, day):
        try:
            week = self.week[day]
            evals = self.eval[int(self.is_eval()['num'])]
            timetable = self.get_user_timetable(self.get_user_course(id), day, self.is_eval()['word'])
            self.bot.send_message(id, 'Расписание на ' + week + ' ('+ evals +')\n\n' + timetable)
        except:
            self.bot.send_message(id, 'Что-то пошло не так, попробуй еще раз зарегистрироваться - /start')

    # ---------------------------

    def is_eval(self):
        if int(datetime.today().strftime("%V")) % 2 == 0:
            return dict(num=1, word=False)
        else:
            return dict(num=0, word=True)

    def today_of_week(self):
        return datetime.today().weekday()

    def get_user_course(self, id):
        try:
            r = requests.get('http://vivers0.pythonanywhere.com/api/user/'+str(id))
            if r.status_code == 200:
                return r.json()['user']['course_id']
        except:
            self.bot.send_message(id, 'Что-то пошло не так, попробуй еще раз зарегистрироваться - /start')

    def get_user_timetable(self, course, day, evall):
        try:
            timetable = requests.get('http://vivers0.pythonanywhere.com/api/timetable/').json()
            for i in timetable['timetable']:
                if i['course_id'] == course:
                    if i['day_week'] == day:
                        if i['is_odd'] == evall:
                            return i['timetable']
        except:
            pass