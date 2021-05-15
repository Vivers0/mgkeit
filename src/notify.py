import asyncio, schedule
from datetime import datetime
from send import Send

class Notify(Send):
    def is_eval(self):
        return 'yes' if int(datetime.today().strftime("%V")) % 2 == 0 else 'no'

    def get_user_timetable(self, course):
        timetable = self.get(self.timetable)
        for el in timetable['res']:
            i = el['fields']
            if i['course_id'] == course:
                if i['day_week'] == datetime.today().weekday():
                    if i['is_odd'] == self.is_eval()['num']:
                        return i['timetable']
    def users(self):
        arr = []
        users = self.get(self.user)
        for user in users['users']:
            if user['notify'] == True:
                arr.append(user)
            print(user)
        return arr

    def get_user_obj(self):
        user = dict()
        for t in self.users():
            user[t['user_id']] = dict(timetable=self.get_user_timetable(t['course_id']), day=datetime.today().weekday())
        return user

    async def notify_main(self):
        def main():
            obj = self.get_user_obj()
            for user in obj:
                timetable = obj[user]['timetable']
                day = self.week[int(obj[user]['day'])]
                self.bot.send_message(user, 'Доброе утро, твое расписание на ' + day + '\n\n' + '\n'.join(timetable))
        schedule.every().day.at('19:42').do(main)
        while True:
            schedule.run_pending()
            await asyncio.sleep(1)