from lesson import Lesson
from ins import Ins
import pandas as pd
import datetime
# from datetime import datetime


# Get a Lesson object by title, if title is not valid, return None
def get_lesson(course, title=None, code=None):
    if title is None and code is None:
        return None

    if code is None:
        if title == 'nan':
            return None
        for l in course.lessons:
            if l.title == title:
                return l

    if title is None:
        for l in course.lessons:
            if l.code == code:
                return l

    return None


def get_ins_by_name(course, name):
    for i in course.ins:
        if i.name == name:
            return i
    return None


# Check if a lesson has Prerequisite.
# Return true if a lesson does not have prerequisite, or prerequisite lesson has been scheduled
def check_pre(lesson, course):
    pre = get_lesson(title=lesson.lessonDf[lesson.lessonDf['Title'].isin([lesson.title])]['Prerequisite'].item(), course=course)
    if pre is None or pre.scheduled is True:
        return True
    return False


def parse_lesson(class_df):
    lessons = []
    for index, row in class_df.iterrows():
        # l = Lesson(title=title, lessonDf=classDf[classDf['Title'].isin([title])])
        l = Lesson(id = row['Id'], title=row['Title'], lesson_df=class_df,
                   code=[class_df[class_df['Title'].isin([row['Title']])]['Sequence'].item(),class_df[class_df['Title'].isin([row['Title']])]['Order'].item()])
        lessons.append(l)
    return lessons


def parse_ins(class_df):
    ins_list = []
    for i in class_df.drop(['Title', 'Sequence', 'Order', 'Id'], axis=1).columns:
        ins_list.append(Ins(i))
    print(ins_list)
    return ins_list


def parse_scheduled(history, course, startdate, classDf):
    # print(history)
    for index, row in history.iterrows():
        if row['Date'] <= str(startdate):
            try:
                cur_lesson_info = classDf[classDf['Id'] == row['Id']]
                history_lesson = Lesson(id = row['Id'], title=cur_lesson_info['Title'].item(), lesson_df=classDf,
                           code=[cur_lesson_info['Sequence'].item(), cur_lesson_info['Order'].item()])
            except:
                print(row)
            course.schedule(date=row['Date'], ins=row['Ins'], lesson=history_lesson)
    print(course.practice_scheduled)
    print(course.class_scheduled)


# Return [lesson, points]
def get_optimal_and_update(course, possible_lessons, calendar_dict, date):
    max_point = -1
    opt_lesson = None
    opt_ins = None
    for l in possible_lessons:
        ins = get_ins(lesson=l, course=course, calendar_dict=calendar_dict, date=date, unavailable_ins=[])
        point = 0
        if str(ins) != 'nan':
            point = l.lesson_df[l.lesson_df['Title'].isin([l.title])][ins.name].item()

        if point > max_point:
            max_point = point
            opt_ins = ins
            opt_lesson = l

    apply_adjustment_lesson(lesson=opt_lesson, ins=opt_ins)
    return [opt_lesson, opt_ins, max_point]


def get_ins(lesson, course, calendar_dict, date, unavailable_ins):
    # drop_list = ['Title', 'Prerequisite'] + unavailableIns
    drop_list = ['Title', 'Sequence', 'Order', 'Id'] + unavailable_ins

   # cur_lesson_df = lesson.lesson_df[lesson.lesson_df['Title'].isin([lesson.title])].drop(drop_list, axis=1)
    cur_lesson_df = apply_adjustment_ins(to_be_scheduled_lesson=lesson, date=date, ins_list=course.ins).drop(drop_list, axis=1)
    ins = cur_lesson_df.idxmax(axis=1).item()

    if date not in calendar_dict:
        calendar_dict[date] = []

    while (ins in calendar_dict[date]) or \
             (date - datetime.timedelta(days=1) in calendar_dict and ins in calendar_dict[date - datetime.timedelta(days=1)]):
        if str(ins) != 'nan':
            unavailable_ins.append(ins)
        ins = get_ins(lesson=lesson, course=course, unavailable_ins=unavailable_ins, calendar_dict=calendar_dict, date=date)

    # print('At {} for class {} ins is {} '.format(date, self.title, ins))
    return get_ins_by_name(course=course, name=ins)


def generate_history(course):
    history = []
    for l in course.class_list:
        history.append([l.date, course.title, l.number, l.id, l.ins])
    pd.DataFrame(history, columns=['Date', 'Course', 'Number', 'Id', 'Ins']).to_csv('Output/' + course.title + '.csv')


def apply_adjustment_ins(to_be_scheduled_lesson, date, ins_list):
    cur_lesson_df = to_be_scheduled_lesson.lesson_df[
        to_be_scheduled_lesson.lesson_df['Id'] == to_be_scheduled_lesson.id]
    for ins in ins_list:
        if ins.has_adjustment():
            point = to_be_scheduled_lesson.lesson_df.loc[to_be_scheduled_lesson.lesson_df.Id == to_be_scheduled_lesson.id, ins.name]
            adj = ins.get_adjustment(date=date)
            if adj != 0 and cur_lesson_df.loc[:, ins.name].item() != 0:
                cur_lesson_df.loc[:, ins.name] += adj
                # print(cur_lesson_df)
                return cur_lesson_df
    return cur_lesson_df


# if an ins is scheduled for a lesson, all following lesson get -0.3 and all other ins get +0.1
def apply_adjustment_lesson(lesson, ins):
    for cur_ins in lesson.lesson_df.loc[lesson.lesson_df.Id == lesson.id].drop(['Title', 'Sequence', 'Order', 'Id'], axis=1):
        if cur_ins == ins.name:
            lesson.lesson_df.loc[lesson.lesson_df[cur_ins] > 0, cur_ins] -= 0.3
        elif lesson.lesson_df.loc[lesson.lesson_df.Id == lesson.id, cur_ins].item() != 0:
            lesson.lesson_df.loc[lesson.lesson_df[cur_ins] > 0, cur_ins] += 0.1

    # print(lesson.lesson_df)