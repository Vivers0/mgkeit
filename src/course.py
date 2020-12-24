from collections import Counter

class Course:
    def __init__(self):
        pass

    def get_course_id(self, msg, build):
        message = Counter(msg.upper())
        if build == 'mill':
            # 1 Поток
            if (message == Counter('1СА-1-20')):
                return 1
            elif (message == Counter('1И-11-20')):
                return 2
            elif (message == Counter('1ИП-1-11-20')):
                return 3
            elif (message == Counter('1СА-2-20')):
                return 4
            elif (message == Counter('1И-20')):
                return 5
            elif (message == Counter('1ИП-1-20')):
                return 6
            elif (message== Counter('1ИП-2-20')):
                return 7
            elif (message == Counter('1ИП-2-11-20')):
                return 8
            elif (message == Counter('1КС-11-20')):
                return 9
            elif (message == Counter('2КС-11-19')):
                return 10
            elif (message == Counter('2ИП-19')):
                return 11
            elif (message == Counter('2И-19')):
                return 12
            elif (message == Counter('2И-11-19')):
                return 13
            elif (message== Counter('2ИП-11-19')):
                return 14
            elif (message == Counter('2СА-19')):
                return 15
            # 2 Поток
            elif (message == Counter('1ЭК-20')):
                return 16
            elif (message == Counter('2ЭК-19')):
                return 17
            elif (message == Counter('1ГД-11-20')):
                return 18
            elif (message == Counter('1ГД-1-20')):
                return 19
            elif (message == Counter('2ГД-19')):
                return 20
            elif (message == Counter('3ГД-18')):
                return 21
            elif (message== Counter('3ЭК-18')):
                return 22
            elif (message == Counter('3ИМ-1-11-18')):
                return 23
            elif (message == Counter('3ИП-2-11-18')):
                return 24
            elif (message == Counter('3ИП-18')):
                return 25
            elif (message == Counter('4ЭК-17')):
                return 26
            elif (message == Counter('3КС-11-18')):
                return 27
            elif (message == Counter('4КС-17')):
                return 28
            elif (message== Counter('1ГД-2-20')):
                return 29
            elif (message == Counter('3СА-18')):
                return 30
            else:
                return 0
        else:
            # 1 Поток
            if (message == Counter('1ЭС-20')):
                return 31
            elif (message == Counter('1ЭМ-2-20')):
                return 32
            elif (message == Counter('1ЭМ-1-20')):
                return 33
            elif (message == Counter('1МИ-20')):
                return 34
            elif (message == Counter('1Р-11-20')):
                return 35
            elif (message == Counter('1Р2-20')):
                return 36
            elif (message == Counter('1Р1-20')):
                return 37
            elif (message == Counter('2Р-11-19')):
                return 38
            elif (message == Counter('2Р-19')):
                return 39
            elif (message == Counter('2МИ-19')):
                return 40
            elif (message == Counter('2ЭС-19')):
                return 41
            elif (message == Counter('2ЭМ-2-19')):
                return 42
            elif (message == Counter('2ЭМ-1-19')):
                return 43
            # 2 Поток
        