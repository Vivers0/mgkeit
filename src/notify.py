import asyncio, schedule
from datetime import datetime
from send import Send
from database import Database

class Notify(Send):
    def is_eval(self):
        return 'yes' if int(datetime.today().strftime("%V")) % 2 == 0 else 'no'

    def get_user_timetable(self, course):
        timetable = self.get(self.timetable)
        for i in timetable['timetable']:
            if i['course_id'] == course:
                if i['day_week'] == datetime.today().weekday():
                    if i['is_odd'] == self.is_eval():
                        return i['timetable']
    def users(self):
        arr = []
        users = self.get(self.user)
        for user in users['users']:
            if user['notify'] == True:
                arr.append(user)
            return arr

    def get_user_obj(self):
        user = dict()
        for t in self.users():
            user[t['user_id']] = dict(timetable=self.get_user_timetable(t['course_id']), day=datetime.today().weekday())
        return user

    async def notify(self):
        obj = self.get_user_obj()
        for user in obj:
            timetable = obj[user]['timetable']
            day = self.week[int(obj[id]['day'])]
            self.bot.send_message(user, 'Доброе утро, твое расписание на ' + day + '\n\n' + timetable)
        try:
            self.get_user_obj()
        except RuntimeWarning:
            pass
        schedule.every().day.at('23:20').do(self.notify)
        while True:
            schedule.run_pending()
            await asyncio.sleep(1)