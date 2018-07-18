from datetime import date
import datetime
import pandas as pd

class DayIter:
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

    def peek(self):
        return self.cur


class Lesson:
    def __init__(self, title, lessonDf, course):
        self.title = title
        self.lessonDf = lessonDf
        self.course = course
        self.scheduled = False

    def schedule(self, date, ins, calendarDict):
        self.scheduled = True
        self.date = date
        self.ins = ins
        self.course.classScheduled += 1
        if self.date in calendarDict:
            calendarDict[self.date].push(ins)
        else:
            calendarDict[self.date] = [ins]

    def getIns(self):
        return self.lessonDf.drop(['Title'], axis=0).idxmax(axis=0)


class Course:

    def __init__(self, title, startDate, weekdys):
        self.title = title
        self.classes = [] # array of lessons
        self.startDate = startDate
        self.iter = DayIter(startDate=startDate, weekdys=str(weekdys))
        self.classScheduled = 0
        self.praClassScheduled = 0



    def schedule(self, scheduleFrom, classInput, practiceInput, calendarDict):

        if scheduleFrom <= self.startDate:
            for title in classInput['Title']:
                print(title)
                lessonDf = classDf[classDf['Title'].isin([title])]
                #lesson = Lesson(title=title, lessonDf=lessonDf, course=)
                # lesson.schedule(date=cur, ins=l.getIns(), calendarDict=calendarDict)


                # lesson.schedule(self.iter.__next__(), )


class Scheduler:
    calendarDict = {}

    def __init__(self):
        pass

    @staticmethod
    def schedule(courses, startDate, classDf):
        cur = startDate
        for x in range(1, 4):
            print(cur)
            for c in courses:
                if c.iter.peek() == cur:
                    l = Lesson(title=classDf.iloc[c.classScheduled]['Title'], lessonDf=classDf.iloc[c.classScheduled], course=c)
                    l.schedule(date=cur, ins=l.getIns(), calendarDict=calendarDict)
                    c.iter.__next__()
                cur += datetime.timedelta(days=1)
        print(calendarDict)






# classInput = pd.read_csv('classInput.csv')
classDf = pd.read_csv('classInput.csv')

print(classDf)

calendarDict = {}

testDate1 = date(2018, 8, 7)
testDate2 = date(2018, 6, 27)
course1 = Course(title='Summer3', startDate=testDate1, weekdys=13567)
course2 = Course(title='Summer2', startDate=testDate2, weekdys=24567)
iter = course1.iter

# for x in range(1, 10):
#    print(iter.__next__())
lessonDf = classDf[classDf['Title'].isin(['Class 01'])]
# print(lessonDf.drop(['Title'], axis=1).idxmax(axis=1))

# print(classDf.iloc[1]['Title'])

# course1.schedule(scheduleFrom=testDate, classInput=classDf)

# print(lessonDf.drop(['Title'], axis=1).idxmax(axis=1))

Scheduler.schedule(courses=[course2], startDate=testDate2, classDf=classDf)

# print(lessonDf.drop(['Title'], axis=1).idxmax(axis=1))



#l = Lesson(title=classDf.iloc[0]['Title'], lessonDf=classDf.iloc[0], course=course1)
#print(classDf.iloc[0])
#print(l.getIns())
#l.schedule(date=testDate, ins=l.getIns(), calendarDict=calendarDict)


