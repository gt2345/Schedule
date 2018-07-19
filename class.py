from datetime import date
import datetime
import time
import pandas as pd

class DayIter:
    def __init__(self, start_date, weekdys):
        self.start_date = start_date
        self.weekdys = list(weekdys)
        self.cur = start_date
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
    def __init__(self, title, lessonDf):
        self.title = title
        self.lessonDf = lessonDf
        # self.course = course
        self.scheduled = False

    def __str__(self):
        if self.scheduled:
            return "%s scheduled at %s for %s" % (self.title, self.date, self.ins)
        else:
            return "%s not scheduled yet" % (self.title)


    def schedule(self, date, calendar_dict):
        self.scheduled = True
        self.date = date
        ins = self.getIns()
        if self.date in calendar_dict:
            unavailableIns = []
            while ins in calendar_dict[self.date]:
                unavailableIns.append(ins)
                ins = self.getIns(unavailableIns=unavailableIns)
            calendar_dict[self.date].append(ins)
        else:
            calendar_dict[self.date] = [ins]
        self.ins = ins

    def getIns(self, unavailableIns=[]):
        drop_list = ['Title'] + unavailableIns
        return self.lessonDf.drop(drop_list, axis=1).idxmax(axis=1).item()



class Course:

    def __init__(self, title, start_date, weekdys, lessons):
        self.title = title
        self.lessons = lessons # array of lessons
        self.start_date = start_date
        self.iter = DayIter(start_date=start_date, weekdys=str(weekdys))
        self.class_list = []
        self.class_scheduled = 0




    def schedule(self, scheduleFrom, classInput, practiceInput, calendarDict):

        if scheduleFrom <= self.start_date:
            for title in classInput['Title']:
                print(title)
                lessonDf = classDf[classDf['Title'].isin([title])]
                #lesson = Lesson(title=title, lessonDf=lessonDf, course=)
                # lesson.schedule(date=cur, ins=l.getIns(), calendarDict=calendarDict)


                # lesson.schedule(self.iter.__next__(), )



def Schedule(courses, start_date):
    calendar_dict = {}
    cur = start_date

    while True:
        done = True
        for c in courses:
            if c.class_scheduled < len(c.lessons):
                done = False
                if c.iter.peek() == cur:
                    l = c.lessons[c.class_scheduled]
                    l.schedule(date=cur, calendar_dict=calendar_dict)
                    c.class_scheduled += 1
                    c.class_list.append([cur, c.title, l.title, l.ins])
                    # l = Lesson(title=classDf.iloc[c.classScheduled]['Title'], lessonDf=classDf.iloc[c.classScheduled], course=c)
                    # l.schedule(date=cur, ins=l.getIns(), calendarDict=calendarDict)
                    c.iter.__next__()

        if done:
            break
        else:
            cur += datetime.timedelta(days=1)
    calendar_df = pd.DataFrame()
    for c in courses:
        if calendar_df.empty:
            calendar_df = pd.DataFrame(c.class_list, columns=['Date', 'Course', 'Class', 'Ins'])
            continue
        calendar_df = pd.merge(calendar_df, pd.DataFrame(c.class_list, columns=['Date', 'Course', 'Class', 'Ins']), how='outer', on='Date', sort='Date')
    return calendar_df


def ParseInput(classDf):
    lessons = []
    for title in classDf['Title']:
        l = Lesson(title=title, lessonDf=classDf[classDf['Title'].isin([title])])
        lessons.append(l)
        # print(str(l))
    return lessons



# create lessons ob
classDf = pd.read_csv('classInput.csv')
lessons = ParseInput(classDf)

# calendarDict = {}


testDate2 = date(2018, 7, 27)
testDate3 = date(2018, 8, 7)
testDate1 = date(2018, 7, 15)
course3 = Course(title='Summer3', start_date=testDate3, weekdys=13567, lessons=ParseInput(classDf))
course2 = Course(title='Summer2', start_date=testDate2, weekdys=24567, lessons=ParseInput(classDf))
course1 = Course(title='Summer1', start_date=testDate1, weekdys=13567, lessons=ParseInput(classDf))
# iter =

# for x in range(1, 10):
#    print(iter.__next__())
# lessonDf = classDf[classDf['Title'].isin(['Class 01'])]
# print(lessonDf.drop(['Title'], axis=1).idxmax(axis=1))

# print(classDf.iloc[1]['Title'])

# course1.schedule(scheduleFrom=testDate, classInput=classDf)

# print(lessonDf.drop(['Title'], axis=1).idxmax(axis=1))

s = Schedule(courses=[course1, course2, course3], start_date=testDate1)
s.to_csv('res.csv')
print(s)
# print(lessonDf.drop(['Title'], axis=1).idxmax(axis=1))


#print(classDf[classDf['Title'].isin(['Class 01'])])
#l = Lesson(title=classDf.iloc[0]['Title'], lessonDf=classDf.iloc[0])
#print(classDf.iloc[0])
#print(l.getIns())
#l.schedule(date=testDate, ins=l.getIns(), calendarDict=calendarDict)

