from lesson import Lesson
from ins import Ins
from schedule import Schedule
import pandas as pd
from datetime import date
import datetime
from schedule_helper_basic import *
# from datetime import datetime


def parse_scheduled(courses, start_date, course_start_date, calendar_dict):
    # pre-process to dataframe
    history = {}
    for course in courses:
        history_df = pd.read_csv(course.title + '_history_final.csv')
        for index, row in history_df.iterrows():
            cur_date_month, cur_date_day, cur_date_year = row['Date'].split('/')
            history_df.loc[index, 'Date'] = date(int(cur_date_year), int(cur_date_month), int(cur_date_day))
        history[course] = history_df
    cur = course_start_date
    while cur < start_date:
        print('cur is {}'.format(cur))
        cur_schedule = Schedule(date=cur)
        for course, history_df in history.items():
            cur_history_df = history_df[history_df['Date'] == cur]

            if not cur_history_df.index.empty:
                # ins = get_ins_by_name(course=course, name=cur_history_df['Ins'].item())
                cur_schedule.add_course(course=course, lesson=get_lesson(course=course, id=cur_history_df['Id'].item()),
                                        ins=get_ins_by_name(course=course, name=cur_history_df['Ins'].item()), point=0,
                                        calendar_dict=calendar_dict)

        if cur_schedule.is_valid():
            print(cur_schedule)
            cur_schedule.schedule_today(calendar_dict=calendar_dict)
            cur_schedule.clean_up(calendar_dict=calendar_dict)
        cur += datetime.timedelta(days=1)


def parse_lesson(class_df):
    lessons = []
    for index, row in class_df.iterrows():
        # l = Lesson(title=title, lessonDf=classDf[classDf['Title'].isin([title])])
        l = Lesson(id = row['Id'], title=row['Title'], lesson_df=class_df,
                   week=row['Week'], code=[row['Sequence'], row['Order']])
                   # code=[class_df[class_df['Title'].isin([row['Title']])]['Sequence'].item(),class_df[class_df['Title'].isin([row['Title']])]['Order'].item()])
        lessons.append(l)
    return lessons


def parse_ins(lesson_df, ins_df):
    ins_list = []
    for i in lesson_df.drop(['Title', 'Sequence', 'Order', 'Id', 'Week'], axis=1).columns:
        ins_list.append(Ins(i))
    for ins in ins_list:
        cur_ins_df = ins_df[ins_df['Ins'] == ins.name]
        if not cur_ins_df.empty:
            if cur_ins_df['adjustment_scale'].item() != 0:
                ins.cur_adjustment_scale = cur_ins_df['adjustment_scale'].item()
            if cur_ins_df['absent_start'].item() != 0:
                cur_start_month, cur_start_day, cur_start_year = cur_ins_df['absent_start'].item().split('/')
                cur_end_month, cur_end_day, cur_end_year = cur_ins_df['absent_end'].item().split('/')
                ins.set_absent(absent_start=date(int(cur_start_year), int(cur_start_month), int(cur_start_day)),
                               absent_end=date(int(cur_end_year), int(cur_end_month), int(cur_end_day)))
            if cur_ins_df['adjustment_weekdays'].item() != 0:
                ins.set_adjustment(weekdys=str(int(cur_ins_df['adjustment_weekdays'].item())),
                                   adjust=cur_ins_df['adjustment_weekdays_points'].item())
            if cur_ins_df['yesterday'].item() != 0:
                ins.yesterday = cur_ins_df['yesterday'].item()
    return ins_list


def parse_pre_scheduled(pre_scheduled, opt_schedule, calendar_dict, cur, second_day, courses):
    drop_course = []
    cur_pre_scheduled = pre_scheduled[pre_scheduled['Date'].isin([str(cur), str(second_day)])]
    if not cur_pre_scheduled.empty:
        for c in courses:
            if not cur_pre_scheduled[cur_pre_scheduled['Course'] == c.title].empty:
                cur_course_pre_scheduled = cur_pre_scheduled[cur_pre_scheduled['Course'] == c.title]
                for one in opt_schedule:
                    if str(one.date) == pre_scheduled['Date'].item():
                        one.add_course(course=c, lesson=get_lesson(course=c,
                                                                   id=cur_course_pre_scheduled['Id'].item()),
                                       ins=get_ins_by_name(course=c, name=cur_course_pre_scheduled['Ins'].item()),
                                       calendar_dict=calendar_dict, point=0)
                drop_course.append(c.title)
    return drop_course
