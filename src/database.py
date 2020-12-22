import sqlite3, os
from course import Course
from timer import Timer
from keybutton import Keybutton
from datetime import datetime
from collections import Counter

class DB:
    def __init__(self, bot):
        self.bot = bot
        self.course = Course()
        self.keybutton = Keybutton(self.bot)
        self.timer = Timer(self.bot)
        self.connect = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'database','database.db'), check_same_thread=False)
        self.cursor = self.connect.cursor()
        self.send = Send(self.bot, self.cursor, self.timer)

    ################
    #
    # Autorisation
    #
    ################

    def check_user_in_db(self, message):
        user_id = message.from_user.id
        res = 'SELECT * FROM users WHERE id = ?'
        self.cursor.execute(res, [user_id,])
        if (len(self.cursor.fetchall()) == 0):
            return False
        else:
            return True
        self.connect.commit()

    def added_user_in_db(self, message):
        if self.check_user_in_db(message) == False:
            user_id = message.from_user.id
            self.cursor.execute('INSERT INTO users (id) VALUES (?)', [user_id,])
            self.connect.commit()
            self.keybutton.send_build(message)
            return True
        else:
            self.bot.reply_to(message, 'Ты уже есть в базе данных 😊')

    def added_user_course(self, message):
        msg = message.text
        user_id = message.from_user.id
        res = 'SELECT build_id FROM users WHERE id = ?'
        self.cursor.execute(res, [user_id,])
        build = self.cursor.fetchone()[0]
        course_id = self.course.get_course_id(msg, build)
        if course_id == 0:
            msg = self.bot.send_message(user_id, 'Я не нашел такого курса 🙁. Попробуй еще раз:)')
            self.bot.register_next_step_handler(msg, self.added_user_course)
        # print(course_id)
        res = 'UPDATE users SET course_id = ? WHERE id = ?'
        self.cursor.execute(res, [course_id, user_id,])
        self.connect.commit()
        self.bot.send_message(user_id, 'Отлично! Если ты хочешь получать уведомления с расписанием каждый день в 7 утра, то просто напиши /notify или нажми на этот текст:)')
        self.keybutton.send_menu(message)

    def added_user_build_id(self, call):
        if call.message:
            if call.data == 'mill':
                user_id = call.message.chat.id
                res = 'UPDATE users SET build_id = ? WHERE id = ?'
                self.cursor.execute(res, ['mill', user_id,])
                self.connect.commit()
                msg = self.bot.send_message(call.message.chat.id, 'Отлично! ☺️ Теперь тебе нужно указать свой курс (Например: 1CА-1-20 или 3ЭК-18)')
                self.bot.register_next_step_handler(msg, self.added_user_course)
            elif call.data == 'sudo':
                user_id = call.message.chat.id
                res = 'UPDATE users SET build_id = ? WHERE id = ?'
                self.cursor.execute(res, ['sudo', user_id,])
                self.connect.commit()
                self.bot.send_message(call.message.chat.id, 'Отлично! ☺️ Теперь тебе нужно указать свой курс (Например: 1CА-1-20 или 3ЭК-18)')
                self.bot.register_next_step_handler(msg, self.added_user_course)
            else:
                self.bot.send_message(call.message.chat.id, 'Я не могу распознать корпус, котрорый 😣, попробуй еще раз!')

    def reset_user_in_db(self, message):
        user_id = message.from_user.id
        self.cursor.execute('DELETE FROM users WHERE id = ?', [user_id,])
        self.connect.commit()
        self.bot.send_message(user_id, 'Я удалил всю информацию о тебе. Теперь тебе нужно заново зарегистрироваться - /start')

        

    ################
    #
    # Timetable
    #
    ################

    def enable_notify(self, message):
        user_id = message.from_user.id
        self.cursor.execute('SELECT notify FROM users WHERE id = ?', [user_id,])
        result = self.cursor.fetchone()
        if result[0] == 'False':
            self.cursor.execute('UPDATE users SET notify = ? WHERE id = ?', ['True', user_id,])
            self.connect.commit()
            self.bot.send_message(user_id, 'Автоматическая отправка расписания: *Включено*')
        else:
            self.cursor.execute('UPDATE users SET notify = ? WHERE id = ?', ['False', user_id,])
            self.connect.commit()
            self.bot.send_message(user_id, 'Автоматическая отправка расписания: *Выключено*')

    def check_user_for_notify(self):
        user = dict()
        def is_eval():
            if int(datetime.today().strftime("%V")) % 2 == 0:
                return 'no'
            else:
                return 'yes'

        def day_of_week():
            return datetime.today().weekday()

        def get_timetable(course):
           self.cursor.execute('SELECT timetable FROM timetable WHERE course_id = ? AND day_week = ? AND is_odd = ?', [course, day_of_week(), is_eval(),])
           return self.cursor.fetchone()[0]

            
        self.cursor.execute('SELECT * FROM users WHERE notify = ?', ['True',])

        for t in self.cursor.fetchall():
            user[t[0]] = dict(timetable=get_timetable(t[1]), day=day_of_week())
        return user

    def get_timetable_button_day(self, message, day):
        user_id = message.from_user.id
        if day == 'today':
            self.send.today_button(user_id)
        elif day == 'tomorrow':
            self.send.tomorrow_button(user_id)

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
    def __init__(self, bot, cursor, timer):
        self.bot = bot
        self.cursor = cursor
        self.timer = timer

    def today_button(self, id):
        week = self.timer.get_weeklist()[int(self.today_of_week())]
        evals = self.timer.get_eval()[int(self.is_eval()['num'])]
        timetable = self.get_user_timetable(self.get_user_course(id), self.today_of_week(), self.is_eval()['word'])
        self.bot.send_message(id, 'Расписание на ' + week + ' ('+ evals +')\n\n' + timetable)

    def tomorrow_button(self, id):
        week = self.timer.get_weeklist()[int(self.today_of_week())+1]
        evals = self.timer.get_eval()[int(self.is_eval()['num'])]
        timetable = self.get_user_timetable(self.get_user_course(id), self.today_of_week()+1, self.is_eval()['word'])
        self.bot.send_message(id, 'Расписание на ' + week + ' ('+ evals +')\n\n' + timetable)

    def another_day(self, id, day):
        week = self.timer.get_weeklist()[day]
        evals = self.timer.get_eval()[int(self.is_eval()['num'])]
        timetable = self.get_user_timetable(self.get_user_course(id), day, self.is_eval()['word'])
        self.bot.send_message(id, 'Расписание на ' + week + ' ('+ evals +')\n\n' + timetable)

    # ---------------------------

    def is_eval(self):
        if int(datetime.today().strftime("%V")) % 2 == 0:
            return dict(num=1, word='no')
        else:
            return dict(num=0, word='yes')

    def today_of_week(self):
        return datetime.today().weekday()

    def get_user_course(self, id):
        self.cursor.execute('SELECT course_id FROM users WHERE id = ?', [id,])
        return self.cursor.fetchone()[0]

    def get_user_timetable(self, course, day, eval):
        self.cursor.execute('SELECT timetable FROM timetable WHERE course_id = ? AND day_week = ? AND is_odd = ?', [course, day, eval,])
        return self.cursor.fetchone()[0]