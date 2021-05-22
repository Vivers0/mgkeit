from datetime import time
from send import Send
from collections import Counter

class Timetable(Send):
    def get_timetable(self, message, day):
        course = self.get_user_course(message)
        # Dolgo
        timetable = self.get(self.timetable)
        if timetable is None:
            return None  
        for el in timetable['res']:
            i = el['fields']
            if i['course_id'] == course:
                if i['day_week'] == day:
                    if i['is_odd'] == self.is_eval()['num']:
                        return i['timetable']

    def another_day_timetable(self, message):
        msg = Counter(str(message.text).upper())
        if msg == Counter('ПОНЕДЕЛЬНИК'):
            return self.get_another_timetable(message, 0)
        elif msg == Counter('ВТОРНИК'):
            return self.get_another_timetable(message, 1)
        elif msg == Counter('СРЕДА'):
            return self.get_another_timetable(message, 2)
        elif msg == Counter('ЧЕТВЕРГ'):
            return self.get_another_timetable(message, 3)
        elif msg == Counter('ПЯТНИЦА'):
            return self.get_another_timetable(message, 4)
        elif msg == Counter('СУББОТА'):
            return self.get_another_timetable(message, 5)
        elif msg == Counter('ВОСКРЕСЕНЬЕ'):
            return self.get_another_timetable(message, 6)
        else:
            pass


    def today_timetable(self, message):
        user_id = message.from_user.id
        week = self.week[self.today_of_week()]
        evals = self.eval[self.is_eval()['num']]
        timetable = self.get_timetable(message, self.today_of_week())
        if not timetable is None:
            try:
                self.bot.send_message(user_id, 'Расписание на ' + week + ' ('+ evals +')\n\n' + "\n".join(timetable))
            except:
                self.bot.send_message(user_id, 'Что-то пошло не так, попробуй еще раз зарегистрироваться - /start')
        else:
            self.bot.send_message(user_id, 'Доброе утро, твое расписание на ' + week + ' ('+ evals +')\n\n' + "Расписание не добавлено в Базу Данных")

    def tomorrow_timetable(self, message):
        user_id = message.from_user.id
        week = self.week[self.today_of_week()+1]
        evals = self.eval[self.is_eval()['num']]
        timetable = self.get_timetable(message, self.today_of_week()+1)
        if not timetable is None:
            try:
                self.bot.send_message(user_id, 'Расписание на ' + week + ' ('+ evals +')\n\n' + "\n".join(timetable))
            except:
                self.bot.send_message(user_id, 'Что-то пошло не так, попробуй еще раз зарегистрироваться - /start')
        else:
            self.bot.send_message(user_id, 'Доброе утро, твое расписание на ' + week + ' ('+ evals +')\n\n' + "Расписание не добавлено в Базу Данных")

    def get_another_timetable(self, message, day):
        user_id = message.from_user.id
        week = self.week[day]
        evals = self.eval[self.is_eval()['num']]
        timetable = self.get_timetable(message, day)
        if not timetable is None:
            try:
                self.bot.send_message(user_id, 'Расписание на ' + week + ' ('+ evals +')\n\n' + "\n".join(timetable))
            except:
                self.bot.send_message(user_id, 'Что-то пошло не так, попробуй еще раз зарегистрироваться - /start')
        else:
            self.bot.send_message(user_id, 'Доброе утро, твое расписание на ' + week + ' ('+ evals +')\n\n' + "Расписание не добавлено в Базу Данных")

