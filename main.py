
from schedule_helper import *
from main_optimization import *
from parse import *

class_input = 'Input/Punch card - Final 0806.csv'

ins_adjustment_input = 'Input/Ins.csv'




def main_schedule(courses, start_date, opt_level, schedule_week, scale_factor):
    calendar_dict = {}
    point = 0
    counter = 0
    point_list = []
    # Schedule start after course start date
    if earliest_course_start_date(courses) < start_date:
        parse_scheduled(courses=courses, start_date=start_date,
                        course_start_date=earliest_course_start_date(courses), calendar_dict=calendar_dict)

    cur = start_date
    while True:
        if schedule_week and cur >= start_date + datetime.timedelta(days=7):
            break
        # print('Today date {}'.format(cur))
        # for one day, schedule with different order
        opt_schedule_list = optimization(opt_level=opt_level, cur=cur, courses=courses, calendar_dict=calendar_dict, scale_factor=scale_factor)
        # process opt schedule list
        for tmp in opt_schedule_list:
            point += opt_schedule_list[tmp].point
            point_list.append(opt_schedule_list[tmp].point)
            counter += len(opt_schedule_list[tmp].schedule)
        if len(opt_schedule_list) == 0:
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% not able to schedule %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            print(datetime.datetime.now() - start)
            break
        for key in opt_schedule_list:
            if opt_schedule_list[key].is_valid():
                # print('Actually scheduled here {}'.format(opt_schedule_list[key]))
                opt_schedule_list[key].schedule_today(calendar_dict=calendar_dict)

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
    calendar_df.to_csv('Output/res.csv')
    #print('point: {}'.format(point))
    #print('counter: {}'.format(counter))
    print(calendar_dict)
    return point, counter, point_list


start = datetime.datetime.now()
# create lessons ob
lesson_df = pd.read_csv(class_input).fillna(0)

# create job ob
ins_list = parse_ins(lesson_df, ins_df=pd.read_csv(ins_adjustment_input).fillna(0))

testDate1 = date(2018, 9, 19)
testDate2 = date(2018, 6, 30)
testDate3 = date(2018, 8, 11)
schedule_from = date(2018, 10, 1)

Fall1 = Course(title='Fall01', start_date=testDate1, weekdys=13567,
                lessons=parse_lesson(lesson_df), ins=get_ins_list(ins_list=ins_list, ins_array=['Jin']), unavailable_ins = ['Jin'])
course2 = Course(title='Summer02', start_date=testDate2, weekdys=13567,
                 lessons=parse_lesson(lesson_df), ins=get_ins_list(ins_list=ins_list, ins_array=['Jin']),
                 unavailable_ins = ['Jin'])
course3 = Course(title='Summer03', start_date=testDate3, weekdys=24567,
                 lessons=parse_lesson(lesson_df), ins=get_ins_list(ins_list=ins_list, ins_array=['Joe']),
                 unavailable_ins = ['Joe'])
opt_level = 4
schedule_week = True
scale_factor = 0.5
main_schedule(courses=[course3, Fall1], start_date=schedule_from, opt_level=opt_level, schedule_week=schedule_week, scale_factor=scale_factor)
quit(12)
res = []
for level in range(7):
    scale_factor = 0
    while scale_factor <= 1:
        ins_list = parse_ins(lesson_df, ins_df=pd.read_csv(ins_adjustment_input).fillna(0))
        course2 = Course(title='Summer02', start_date=testDate2, weekdys=13567,
                         lessons=parse_lesson(lesson_df), ins=get_ins_list(ins_list=ins_list, ins_array=['Jin']),
                         unavailable_ins=['Jin'])
        course3 = Course(title='Summer03', start_date=testDate3, weekdys=24567,
                         lessons=parse_lesson(lesson_df), ins=get_ins_list(ins_list=ins_list, ins_array=['Joe']),
                         unavailable_ins=['Joe'])
        print('scale_factor = {}'.format(scale_factor))
        print('level = {}'.format(level + 1))

        start = datetime.datetime.now()
        point, counter, point_list = main_schedule(courses=[course2, course3], start_date=schedule_from, opt_level=level + 1,
                      schedule_week=schedule_week, scale_factor=scale_factor)
        dur = datetime.datetime.now() - start

        print('dur = {}'.format(dur))
        print('point = {}'.format(point_list))
        res.append([scale_factor, level + 1, point, counter, dur, str(point_list)])
        scale_factor += 0.1
pd.DataFrame(res, columns=['scale_factor', 'level', 'point', 'counter', 'dur', 'point_list']).to_csv('Output/graph.csv')





