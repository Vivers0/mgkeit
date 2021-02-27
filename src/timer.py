import schedule, time, asyncio
from datetime import date

class Timer:
    def __init__(self):
        self.eval = ['Четная', 'Нечетная']
        self.week = ['Понедельник', 'Вторник', 'Среду', 'Четверг', 'Пятницу', 'Субботу', 'Воскресенье']

    # async def sending_messages_with_timetable(self, obj):
    #     def sending_message():
    #         for id in obj:
    #             timetable = obj[id]['timetable']
    #             day = self.week[int(obj[id]['day'])]
    #             self.bot.send_message(id, 'Доброе утро , твое расписание на ' + day + '\n\n' + timetable)
    #     self.database.check_user_for_notify()

    #     schedule.every().day.at("14:52").do(sending_message)
    #     while True:
    #         schedule.run_pending()
    #         await asyncio.sleep(1)

    def get_weeklist(self):
        return self.week
    def get_eval(self):
        return self.eval