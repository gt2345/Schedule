import datetime
from course import Course
from itertools import permutations
from schedule_helper import *
from parse import *


def main_schedule(courses, start_date):
    calendar_dict = {}
    # Schedule start after course start date
    if earliest_course_start_date(courses) < start_date:
        parse_scheduled(courses=courses, start_date=start_date,
                        course_start_date=earliest_course_start_date(courses), calendar_dict=calendar_dict)

    all_courses_permu = list(permutations(courses))
    cur = start_date
    while True:
        print('Today date {}'.format(cur))
        opt_schedule = Schedule(date=None)
        # for one day, schedule with different order
        for course_list in all_courses_permu:
            cur_schedule = get_one_schedule(courses=course_list, cur_date=cur, calendar_dict=calendar_dict)
            if cur_schedule.better_than(opt_schedule):
                opt_schedule = cur_schedule

        if opt_schedule.is_valid():
            print('Actually scheduled')
            print(opt_schedule)
            print(opt_schedule.point)
            opt_schedule.schedule_today(calendar_dict=calendar_dict)

        if cur.year > 2018 or check_complete(courses=courses):
            break
        else:
            cur += datetime.timedelta(days=1)

    # post processing
    for c in courses:
        generate_history(course=c)

    # generate calendar to use for csv
    calendar_df = pd.DataFrame()
    for c in courses:
        calendar_list = []
        for l in c.class_list:
            calendar_list.append([l.date, c.title, l.number, l.title, l.ins])
        if calendar_df.empty:
            calendar_df = pd.DataFrame(calendar_list, columns=['Date', 'Course', 'Number', 'Class', 'Ins'])
        else:
            calendar_df = pd.merge(calendar_df,
                                   pd.DataFrame(calendar_list,columns=['Date', 'Course', 'Number', 'Class', 'Ins']),
                                   how='outer', on='Date', sort='Date')
    return calendar_df


# create lessons ob
lesson_df = pd.read_csv('Input/Punch card - Final 0802.csv').fillna(0)

# create job ob
ins_list = parse_ins(lesson_df)
for ins in ins_list:
    if ins.name == 'Tang':
        ins.set_adjustment('567', 4)
    if ins.name == 'Lu':
        ins.set_adjustment('1', -20)
    if ins.name == 'Zhao':
        ins.cur_adjustment_scale = 1.5
    if ins.name == 'Sun':
        ins.set_absent(absent_start=date(2018, 8, 20), absent_end=date(2018, 9, 20))

testDate1 = date(2018, 5, 26)
testDate2 = date(2018, 6, 30)
testDate3 = date(2018, 8, 11)
schedule_from = date(2018, 8, 20)

course3 = Course(title='Summer03', start_date=testDate3, weekdys=24567, lessons=parse_lesson(lesson_df), ins=ins_list)
course2 = Course(title='Summer02', start_date=testDate2, weekdys=13567, lessons=parse_lesson(lesson_df), ins=ins_list)
course1 = Course(title='Summer01', start_date=testDate1, weekdys=24567, lessons=parse_lesson(lesson_df), ins=ins_list)

s = main_schedule(courses=[course1, course2, course3], start_date=schedule_from)
s.to_csv('Output/res.csv')



