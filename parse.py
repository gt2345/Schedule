from lesson import Lesson
from schedule import Schedule
from datetime import date
from helper import *
from get_lessons import *
from get_ins import *


def parse_scheduled(courses, start_date, course_start_date, calendar_dict):
    # pre-process to dataframe
    history = {}
    for course in courses:
        if course.start_date > start_date:
            continue
        history_df = pd.read_csv('Output/' + course.title + '_history_cleaned.csv')
        for index, row in history_df.iterrows():
            if '/' in row['Date']:
                cur_date_month, cur_date_day, cur_date_year = row['Date'].split('/')
            else:
                cur_date_year, cur_date_month, cur_date_day = row['Date'].split('-')
            history_df.loc[index, 'Date'] = date(int(cur_date_year), int(cur_date_month), int(cur_date_day))
        history[course] = history_df
    cur = course_start_date
    while cur < start_date:
        cur_schedule = Schedule(date=cur)
        for course, history_df in history.items():
            cur_history_df = history_df[history_df['Date'] == cur]

            if not cur_history_df.index.empty:
                cur_schedule.add_course(course=course, lesson=get_lesson(course=course, id=cur_history_df['Id'].item()),
                                        ins=get_ins_by_name(course=course, name=cur_history_df['Ins'].item()), point=0,
                                        calendar_dict=calendar_dict)

        if cur_schedule.is_valid():
            cur_schedule.schedule_today(calendar_dict=calendar_dict)
        cur += datetime.timedelta(days=1)


def parse_lesson(lesson_df):
    lessons = []
    for index, row in lesson_df.iterrows():
        l = Lesson(id = row['Id'], title=row['Title'], lesson_df=lesson_df,
                   week=row['Week'], code=[row['Sequence'], row['Order']])
        lessons.append(l)
    return lessons


def parse_ins(lesson_df, ins_df):
    ins_list = []
    for i in lesson_df.drop(['Title', 'Sequence', 'Order', 'Id', 'Week'], axis=1).columns:
        ins_list.append(Ins(i))
    for ins in ins_list:
        cur_ins_df = ins_df[ins_df['Ins'] == ins.name]
        if not cur_ins_df.empty:
            for _, row in cur_ins_df.iterrows():
                if row['adjustment_scale'] != 0:
                    ins.cur_adjustment_scale = row['adjustment_scale']
                if row['absent_start'] != 0:
                    cur_start_month, cur_start_day, cur_start_year = row['absent_start'].split('/')
                    cur_end_month, cur_end_day, cur_end_year = row['absent_end'].split('/')
                    ins.set_absent(absent_start=date(int(cur_start_year), int(cur_start_month), int(cur_start_day)),
                                   absent_end=date(int(cur_end_year), int(cur_end_month), int(cur_end_day)))
                if row['adjustment_weekdays'] != 0:
                    ins.set_adjustment(weekdys=str(int(row['adjustment_weekdays'])),
                                       adjust=row['adjustment_weekdays_points'])
                if row['yesterday'] != 0:
                    ins.yesterday = row['yesterday']
                if row['max_per_week'] != 0:
                    ins.max_per_week = row['max_per_week']
    return ins_list


def parse_pre_scheduled(pre_scheduled, calendar_dict, cur, courses, opt_level, ret_opt_schedule_list):
    drop_course = []
    if pre_scheduled.empty:
        return drop_course
    counter = 0
    while counter < opt_level:
        cur_date = cur + datetime.timedelta(days=counter)
        cur_pre_scheduled = pre_scheduled[pre_scheduled['Date'] == str(cur_date)]
        if not cur_pre_scheduled.empty:
            if cur_date not in ret_opt_schedule_list:
                ret_opt_schedule_list[cur_date] = Schedule(date=cur_date)
            for c in courses:
                if not cur_pre_scheduled[cur_pre_scheduled['Course'] == c.title].empty:
                    cur_course_pre_scheduled = cur_pre_scheduled[cur_pre_scheduled['Course'] == c.title]
                    ret_opt_schedule_list[cur_date].add_course(course=c, lesson=get_lesson(course=c,
                                                                   id=cur_course_pre_scheduled['Id'].item()),
                                       ins=get_ins_by_name(course=c, name=cur_course_pre_scheduled['Ins'].item()),
                                       calendar_dict=calendar_dict, point=0)
                    get_lesson(course=c, id=cur_course_pre_scheduled['Id'].item()).pre_scheduled = True
                    drop_course.append(c)
        counter += 1

    return drop_course




