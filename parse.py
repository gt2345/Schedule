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
        cur_schedule = Schedule(date=cur)
        for course, history_df in history.items():
            cur_history_df = history_df[history_df['Date'] == cur]

            if not cur_history_df.index.empty:
                # ins = get_ins_by_name(course=course, name=cur_history_df['Ins'].item())
                cur_schedule.add_course(course=course, lesson=get_lesson(course=course, id=cur_history_df['Id'].item()),
                                        ins=get_ins_by_name(course=course, name=cur_history_df['Ins'].item()), point=0,
                                        calendar_dict=calendar_dict)

        if cur_schedule.is_valid():
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


def parse_ins(class_df):
    ins_list = []
    for i in class_df.drop(['Title', 'Sequence', 'Order', 'Id', 'Week'], axis=1).columns:
        ins_list.append(Ins(i))
    print(ins_list)
    return ins_list