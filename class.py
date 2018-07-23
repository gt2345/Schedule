from datetime import date
import datetime
import random
import pandas as pd
from course import Course
from schedule_helper import *


def schedule(courses, start_date):
    calendar_dict = {}
    cur = start_date

    while True:
        done = True
        for c in courses:
            if c.class_scheduled < len(c.lessons[0]) or c.practice_scheduled < len(c.lessons[1]):
                done = False
                if c.iter.peek() == cur:
                    if c.class_scheduled < len(c.lessons[0]) and c.practice_scheduled < len(c.lessons[1]):
                        rand = random.random()

                        if rand <= 0.5:
                            l = c.lessons[0][c.class_scheduled]
                            if check_pre(lesson=l, course=c):
                                c.class_scheduled += 1
                            else:
                                l = c.lessons[1][c.practice_scheduled]
                                if check_pre(lesson=l, course=c):
                                    c.practice_scheduled += 1
                                else:
                                    print(l)
                                    print('Not Able to Schedule')
                                    quit(1)
                        else :
                            l = c.lessons[1][c.practice_scheduled]
                            if check_pre(lesson=l, course=c):
                                c.practice_scheduled += 1
                            else:
                                l = c.lessons[0][c.class_scheduled]
                                if check_pre(lesson=l, course=c):
                                    c.class_scheduled += 1
                                else:
                                    print(l)
                                    print('Not Able to Schedule')
                                    quit(2)
                    elif c.class_scheduled < len(c.lessons[0]):
                        l = c.lessons[0][c.class_scheduled]
                        if check_pre(lesson=l, course=c):
                            c.class_scheduled += 1
                        else:
                            print(l)
                            print('Not Able to Schedule')
                            quit(3)
                    else:
                        l = c.lessons[1][c.practice_scheduled]
                        if check_pre(lesson=l, course=c):
                            c.practice_scheduled += 1
                        else:
                            print(l)
                            print('Not Able to Schedule')
                            quit(4)

                    l.schedule(date=cur, calendar_dict=calendar_dict)
                    c.class_list.append([cur, c.title, l.title, l.ins])
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



# create lessons ob
classDf = pd.read_csv('classInput.csv')
practiceDf = pd.read_csv('practiceInput.csv')


testDate1 = date(2018, 5, 21)
testDate2 = date(2018, 6, 27)
testDate3 = date(2018, 8, 7)

course3 = Course(title='Summer3', start_date=testDate3, weekdys=13567, lessons=[parse_input(classDf), parse_input(practiceDf)])
course2 = Course(title='Summer2', start_date=testDate2, weekdys=24567, lessons=[parse_input(classDf), parse_input(practiceDf)])
course1 = Course(title='Summer1', start_date=testDate1, weekdys=13567, lessons=[parse_input(classDf), parse_input(practiceDf)])

s = schedule(courses=[course1, course2, course3], start_date=testDate1)
s.to_csv('res.csv')
print(s)

