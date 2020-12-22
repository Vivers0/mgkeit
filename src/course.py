from collections import Counter

class Course:
    def __init__(self):
        pass

    def get_course_id(self, msg, build):
        if build == 'mill':
            # 1 Корпус
            if (Counter(msg.upper()) == Counter('1СА-1-20')):
                return 1
            elif (Counter(msg.upper()) == Counter('1И-11-20')):
                return 2
            elif (Counter(msg.upper()) == Counter('1ИП-1-11-20')):
                return 3
            elif (Counter(msg.upper()) == Counter('1СА-2-20')):
                return 4
            elif (Counter(msg.upper()) == Counter('1И-20')):
                return 5
            elif (Counter(msg.upper()) == Counter('1ИП-1-20')):
                return 6
            elif (Counter(msg.upper()) == Counter('1ИП-2-20')):
                return 7
            elif (Counter(msg.upper()) == Counter('1ИП-2-11-20')):
                return 8
            elif (Counter(msg.upper()) == Counter('1КС-11-20')):
                return 9
            elif (Counter(msg.upper()) == Counter('2КС-11-19')):
                return 10
            elif (Counter(msg.upper()) == Counter('2ИП-19')):
                return 11
            elif (Counter(msg.upper()) == Counter('2И-19')):
                return 12
            elif (Counter(msg.upper()) == Counter('2И-11-19')):
                return 13
            elif (Counter(msg.upper()) == Counter('2ИП-11-19')):
                return 14
            elif (Counter(msg.upper()) == Counter('2СА-19')):
                return 15
            else:
                return 0
            # 2 Корпус

        