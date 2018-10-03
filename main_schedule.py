from main_optimization import *
from helper import *


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
    num_level = get_percentage_scale(schedule_week=schedule_week, opt_level=opt_level, courses=courses)
    while True:
        if schedule_week > 0 and cur >= start_date + datetime.timedelta(days=7 * schedule_week):
            break
        if cur >= start_date + datetime.timedelta(days=6):
            break

        # for one day, schedule with different order
        opt_schedule_list = optimization(opt_level=opt_level, cur=cur, courses=courses, calendar_dict=calendar_dict,
                                         scale_factor=scale_factor,
                                         num_level = num_level)
        # process opt schedule list
        for tmp in opt_schedule_list:
            point += opt_schedule_list[tmp].point
            point_list.append(opt_schedule_list[tmp].point)
            counter += len(opt_schedule_list[tmp].schedule)
        if len(opt_schedule_list) == 0:
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% not able to schedule %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
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
        generate_history(course=c, start_date=start_date)

    # generate calendar as csv
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
    #calendar_df.to_csv('Output/res.csv')
    #print('point: {}'.format(point))
    #print('counter: {}'.format(counter))

    return point, counter, point_list

