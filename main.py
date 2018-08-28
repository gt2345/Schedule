from itertools import permutations
from schedule_helper import *
from main_optimization import *
from parse import *

class_input = 'Input/Punch card - Final 0806.csv'

ins_adjustment_input = 'Input/Ins.csv'

stop_date = date(2018, 10, 3)
opt_level = 4


def main_schedule(courses, start_date):
    calendar_dict = {}
    first = 0
    second = 0
    # Schedule start after course start date
    if earliest_course_start_date(courses) < start_date:
        parse_scheduled(courses=courses, start_date=start_date,
                        course_start_date=earliest_course_start_date(courses), calendar_dict=calendar_dict)

    all_courses_permu = list(permutations(courses))
    cur = start_date
    while True:
        print('Today date {}'.format(cur))

        # opt_schedule = [Schedule(date=cur), Schedule(date=second_day)]
        # if one lesson is pre-scheduled

        drop_course = []
        # for one day, schedule with different order
        opt_schedule_list = optimization(opt_level=opt_level, cur=cur, courses=courses, calendar_dict=calendar_dict)
        for key in opt_schedule_list:
            if opt_schedule_list[key].is_valid():
                print('Actually scheduled here {}'.format(opt_schedule_list[key]))
                opt_schedule_list[key].schedule_today(calendar_dict=calendar_dict)
                print(calendar_dict)

        if cur.year > 2018 or check_complete(courses=courses):
            break
        else:
            cur += datetime.timedelta(days=opt_level)

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


start = datetime.datetime.now()
# create lessons ob
lesson_df = pd.read_csv(class_input).fillna(0)

# create job ob
ins_list = parse_ins(lesson_df, ins_df=pd.read_csv(ins_adjustment_input).fillna(0))

testDate1 = date(2018, 5, 26)
testDate2 = date(2018, 6, 30)
testDate3 = date(2018, 8, 11)
schedule_from = date(2018, 9, 10)

course1 = Course(title='Summer01', start_date=testDate1, weekdys=24567,
                 lessons=parse_lesson(lesson_df), ins=ins_list, unavailable_ins=[])
course2 = Course(title='Summer02', start_date=testDate2, weekdys=13567,
                 lessons=parse_lesson(lesson_df), ins=get_ins_list(ins_list=ins_list, ins_array=['Jin']),
                 unavailable_ins = ['Jin'])
course3 = Course(title='Summer03', start_date=testDate3, weekdys=24567,
                 lessons=parse_lesson(lesson_df), ins=get_ins_list(ins_list=ins_list, ins_array=['Joe']),
                 unavailable_ins = ['Joe'])

s = main_schedule(courses=[course2, course3], start_date=schedule_from)
s.to_csv('Output/res.csv')

dur = datetime.datetime.now() - start
print(dur)

