import schedule, time, asyncio
from datetime import date

class Timer:
    def __init__(self):
        self.eval = ['Четная', 'Нечетная']
        self.week = ['Понедельник', 'Вторник', 'Среду', 'Четверг', 'Пятницу', 'Субботу', 'Воскресенье']

    def get_weeklist(self):
        return self.week
    def get_eval(self):
        return self.eval