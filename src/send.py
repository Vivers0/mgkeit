from datetime import datetime
from database import Database

class Send(Database):
    def today_of_week(self):
        return datetime.today().weekday()
    def is_eval(self):
        return dict(num=1, word=False) if int(datetime.today().strftime("%V")) % 2 == 0 else dict(num=0, word=True)
