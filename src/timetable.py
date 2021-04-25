from send import Send

class Timetable(Send):
    def today_timetable(self, message):
        course = 
        timetable = self.get(self.timetable)
        for i in timetable['timetable']:
            if i['course_id'] == course:
                if i['day_week'] == self.today_of_week():
                    if i['is_odd'] == self.is_eval()['num']:
                        return i['timetable']
    def tomorrow_timetable(self, message):
        timetable = self.get(self.timetable)
        for i in timetable['timetable']:
            if i['course_id'] == course:
                if i['day_week'] == self.today_of_week()+1:
                    if i['is_odd'] == self.is_eval()['num']:
                        return i['timetable']
