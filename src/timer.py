import calendar
import schedule
import time, asyncio
from datetime import date


class Timer:
    def __init__(self, bot):
        self.bot = bot
        self.eval = ['Четная', 'Нечетная']
        self.week = ['Понедельник', 'Вторник', 'Среду', 'Четверг', 'Пятницу', 'Субботу', 'Воскресенье']

    async def sending_messages_with_timetable(self, obj):
        def sending_message(id):
            for res in obj:
                id = res
                timetable = obj[res]['timetable']
                day = self.week[int(obj[res]['day'])]
                # print(obj[res][day])
                self.bot.send_message(id, 'Доброе утро , твое расписание на ' + day + '\n\n' + timetable)


        schedule.every().day.at("11:46").do(sending_message, obj)
        while True:
            schedule.run_pending()
            await asyncio.sleep(1)


    # def today(self):
    #     my_date = date.today()
    #     return self.week[my_date.weekday()]
        

    # def tomorrow(self):
    #     my_date = date.today()
    #     return self.week[my_date.weekday()+1]

    def get_weeklist(self):
        return self.week
    def get_eval(self):
        return self.eval