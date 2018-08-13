import datetime
from course import Course
from itertools import permutations
from schedule_helper import *
from parse import *

class_input = 'Input/Punch card - Final 0806.csv'
pre_scheduled_input = 'pre_scheduled.csv'


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
        opt_schedule = Schedule(date=cur)
        # if one lesson is pre-scheduled
        pre_scheduled = pd.read_csv(pre_scheduled_input)
        drop_course = []
        if not pre_scheduled.empty and not pre_scheduled[pre_scheduled['Date'] == str(cur)].empty:
            print('################################################')
            cur_pre_scheduled = pre_scheduled[pre_scheduled['Date'] == str(cur)]
            for c in courses:
                if not cur_pre_scheduled[cur_pre_scheduled['Course'] == c.title].empty:
                    cur_course_pre_scheduled = cur_pre_scheduled[cur_pre_scheduled['Course'] == c.title]
                    opt_schedule.add_course(course=c,
                                            lesson=get_lesson(course=c, id=cur_course_pre_scheduled['Id'].item()),
                                            ins=get_ins_by_name(course=c, name=cur_course_pre_scheduled['Ins'].item()),
                                            calendar_dict=calendar_dict,
                                            point=0)
                    drop_course.append(c.title)

        # for one day, schedule with different order
        for course_list in all_courses_permu:
            print(course_list)
            cur_schedule = get_one_schedule(courses=course_list, cur_date=cur,
                                            calendar_dict=calendar_dict, drop_list=drop_course)
            if cur_schedule.better_than(opt_schedule):
                opt_schedule.update(cur_schedule)

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
lesson_df = pd.read_csv(class_input).fillna(0)

# create job ob
ins_list = parse_ins(lesson_df)
for ins in ins_list:
    if ins.name == 'Tang':
        ins.set_adjustment('567', 4)
    if ins.name == 'Lu':
        ins.set_adjustment('1', -20)
    if ins.name == "Jin":
        ins.set_adjustment('12347', -20)
    if ins.name == 'Zhao':
        ins.cur_adjustment_scale = 1.5
    if ins.name == 'Sun':
        ins.set_absent(absent_start=date(2018, 8, 20), absent_end=date(2018, 9, 20))

testDate1 = date(2018, 5, 26)
testDate2 = date(2018, 6, 30)
testDate3 = date(2018, 8, 11)
schedule_from = date(2018, 8, 20)

course1 = Course(title='Summer01', start_date=testDate1, weekdys=24567,
                 lessons=parse_lesson(lesson_df), ins=ins_list)
course2 = Course(title='Summer02', start_date=testDate2, weekdys=13567,
                 lessons=parse_lesson(lesson_df), ins=get_ins_list(ins_list=ins_list, ins_array=['Jin']))
course3 = Course(title='Summer03', start_date=testDate3, weekdys=24567,
                 lessons=parse_lesson(lesson_df), ins=get_ins_list(ins_list=ins_list, ins_array=['Joe']))

s = main_schedule(courses=[course1, course2, course3], start_date=schedule_from)
s.to_csv('Output/res.csv')



