from datetime import date
import datetime
import pandas as pd

class dayIter:
    def __init__(self, startDate, weekdys):
        self.startDate = startDate
        self.weekdys = list(weekdys)
        self.cur = startDate

        while True:
            # print(self.cur.isoweekday())
            if str(self.cur.isoweekday()) in self.weekdys:
                return
            self.cur += datetime.timedelta(days=1)

    def __next__(self):
        res = self.cur
        self.cur += datetime.timedelta(days=1)
        while True:
            if str(self.cur.isoweekday()) in self.weekdys:
                break
            self.cur += datetime.timedelta(days=1)
        return res


class Course:

    class Lesson:
        def __init__(self, title):
            self.title = title
            self.scheduled = False

        def schedule(self, date, ins, calendarDict):
            self.scheduled = True
            self.date = date
            self.ins = ins
            if self.date in calendarDict:
                calendarDict[self.date].push(ins)
            else:
                calendarDict[self.date] = [ins]

        @staticmethod
        def getIns(inputDf):
            ins = inputDf.idxmax(axis=1)

    def __init__(self, title, startDate, weekdys):
        self.title = title
        self.classes = [] # array of lessons
        self.startDate = startDate
        self.iter = dayIter(startDate=testDate, weekdys=str(weekdys))
        self.classScheduled = 0
        self.praClassScheduled = 0

    def schedule(self, scheduleFrom, classInput, practiceInput, calendarDict):

        if scheduleFrom <= self.startDate:
            for title in classInput['Title']:
                lesson = self.Lesson(title)

                # lesson.schedule(self.iter.__next__(), )





classInput = [['Class 01', 10, 8],
         ['Class 02', 10, 8],
         ['Class 03', 10, 8]]
classDf = pd.DataFrame(classInput,columns=['Title', 'Sun', 'Zhao'],dtype=float)

practiceInput = [['Practice 01', 10, 8],
                 ['Practice 02', 10, 8],
                 ['Practice 03', 10, 8]]
practiceDf = pd.DataFrame(practiceInput,columns=['Title', 'Lu', 'Jerry'],dtype=float)

print(classDf)
# print(practiceDf)

calendarDict = {}

testDate = date(2018, 8, 7)
course1 = Course(title='Summer3', startDate=testDate, weekdys=13567)
#print(classDf['Title'])
# course1.schedule(scheduleFrom=testDate, classInput=classDf, practiceInput=practiceDf)
for x in classDf['Title']:
    print(x)

print(classDf['Title']['Class 01'])


