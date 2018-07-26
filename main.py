from datetime import date
import datetime
# from datetime import datetime
import time
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
            if c.class_scheduled <= c.class_total and c.practice_scheduled <= c.practice_total:
                done = False
                if c.iter.peek() == cur:
                    possible_lessons = []
                    for l in c.lessons:
                        if not l.scheduled:
                            # Practice Class 01 corner case
                            if l.code[0] == 1:
                                if l.code[1] == 1 and not get_lesson(course=c, code=[1, 1]).scheduled:
                                    possible_lessons.append(l)
                                    break
                                elif get_lesson(course=c, code=[1, 1]).scheduled:
                                    possible_lessons.append(l)
                                    continue

                            elif (l.code[1] == 0 and get_lesson(course=c, code=[l.code[0] - 1, 1]).scheduled) or \
                                    (l.code[1] > 1 and get_lesson(course=c, code=[l.code[0], l.code[1] - 1]).scheduled) or \
                                    (l.code[1] == 1 and get_lesson(course=c, code=[l.code[0] - 1, 1]).scheduled):
                                possible_lessons.append(l)
                                continue
                    print(c.title)
                    print(possible_lessons)
                    if len(possible_lessons) == 0:
                        print(cur)
                        print('Not Able to Schedule')
                        print('Class scheduled {}'.format(c.class_scheduled))
                        print('Class total {}'.format(c.class_total))
                        print('Practice scheduled {}'.format(c.practice_scheduled))
                        print('Practice total {}'.format(c.practice_total))
                        quit(99)
                    else:
                        # lesson = possible_lessons[1]
                        opt_retval = get_optimal_and_update(possible_lessons=possible_lessons, calendar_dict=calendar_dict, date=cur)
                        lesson = opt_retval[0]
                        ins = opt_retval[1]
                        if str(ins) != 'nan':
                            calendar_dict[cur].append(ins)
                        # print('points: {}'.format(opt_retval[2]))
                    # l.schedule(date=cur, calendar_dict=calendar_dict)
                    c.schedule(lesson=lesson, date=cur, ins=ins)
                    # c.class_list.append([cur, c.title, l.number, l.title, l.ins])
                    c.iter.__next__()

        if done:
            break
        else:
            cur += datetime.timedelta(days=1)
    for c in courses:
        for x in c.class_list:
            print(str(x))

    calendar_df = pd.DataFrame()

    for c in courses:
        calendar_list = []
        for l in c.class_list:
            calendar_list.append([l.date, c.title, l.number, l.title, l.ins])
        if calendar_df.empty:
            calendar_df = pd.DataFrame(calendar_list, columns=['Date', 'Course', 'Number', 'Class', 'Ins'])
        else:
            calendar_df = pd.merge(calendar_df,
                                   pd.DataFrame(calendar_list,columns=['Date', 'Course', 'Number', 'Class', 'Ins']),how='outer', on='Date', sort='Date')
    return calendar_df


# create lessons ob
testDf = pd.read_csv('Input/Punch card - Final.csv').fillna(0)

testDate1 = date(2018, 5, 21)
testDate2 = date(2018, 6, 27)
testDate3 = date(2018, 8, 7)

course3 = Course(title='Summer3', start_date=testDate3, weekdys=13567, lessons=parse_input(testDf))
course2 = Course(title='Summer2', start_date=testDate2, weekdys=24567, lessons=parse_input(testDf))
course1 = Course(title='Summer1', start_date=testDate1, weekdys=13567, lessons=parse_input(testDf))

s = schedule(courses=[course1, course2, course3], start_date=testDate1)
s.to_csv('Output/res.csv')
# print(course3.lessons[2].code)


