from lesson import Lesson
from ins import Ins
import pandas as pd
from datetime import date
import datetime
# from datetime import datetime


# Get a Lesson object by title, if title is not valid, return None
def get_lesson(course, title=None, code=None, id=None):
    if title is None and code is None and id is None:
        return None

    if id is not None:
        for l in course.lessons:
            if l.id == id:
                return l

    if title is not None:
        if title == 'nan':
            return None
        for l in course.lessons:
            if l.title == title:
                return l

    if code is not None:
        for l in course.lessons:
            if l.code == code:
                return l

    return None


def get_ins_by_name(course, name):
    for i in course.ins:
        if i.name == name:
            return i
    return None


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


def parse_scheduled(history, course, startdate):
    for index, row in history.iterrows():
        cur_date_month, cur_date_day, cur_date_year = row['Date'].split('/')
        cur_date = date(int(cur_date_year), int(cur_date_month), int(cur_date_day))
        if cur_date <= startdate:
            history_lesson = get_lesson(course=course, id=row['Id'])
            course.schedule(date=cur_date, ins=row['Ins'], lesson=history_lesson)

    print(course.title)
    print('Practice Class Scheduled: {}'.format(course.practice_scheduled))
    print(course.class_scheduled)


# Return [lesson, ins, points]
def get_optimal_and_update(course, possible_lessons, calendar_dict, date):
    max_point = -1
    opt_lesson = None
    opt_ins = None
    for l in possible_lessons:
        get_ins_ret = get_ins(lesson=l, course=course, calendar_dict=calendar_dict, date=date, unavailable_ins=[])
        ins = get_ins_ret[0]
        point = get_ins_ret[1]
        #print('point: {}'.format(point))
        if point > max_point:
            max_point = point
            opt_ins = ins
            opt_lesson = l

    if opt_ins is not None:
        apply_adjustment_lesson(lesson=opt_lesson, ins=opt_ins)
        print('chosen lesson {}'.format(opt_lesson))
        print('chosen ins {}'.format(opt_ins))
    return [opt_lesson, opt_ins, max_point]


def get_ins(lesson, course, calendar_dict, date, unavailable_ins):
    drop_list = ['Title', 'Sequence', 'Order', 'Id', 'Week'] + unavailable_ins
    cur_lesson_df = apply_adjustment_ins(to_be_scheduled_lesson=lesson, date=date, ins_list=course.ins).drop(drop_list, axis=1)
    ins = get_ins_by_name(course=course, name=cur_lesson_df.idxmax(axis=1).item())
    if(course.title is 'Summer02'):
        print(lesson.title)
        print(cur_lesson_df)
        print('{} at {}'.format(ins.name, date))
        print('******************************************')
    if date not in calendar_dict:
        calendar_dict[date] = []

    while (ins.name in calendar_dict[date]) or \
             (date - datetime.timedelta(days=1) in calendar_dict and ins.name in calendar_dict[date - datetime.timedelta(days=1)]):
        if ins is not None:
            unavailable_ins.append(ins.name)
        ins = get_ins(lesson=lesson, course=course, unavailable_ins=unavailable_ins, calendar_dict=calendar_dict, date=date)[0]

    # print('At {} for class {} ins is {} '.format(date, self.title, ins))
    return [ins, cur_lesson_df[ins.name].item()]


def generate_history(course):
    history = []
    for l in course.class_list:
        history.append([l.date, course.title, l.number, l.id, l.ins])
    pd.DataFrame(history, columns=['Date', 'Course', 'Number', 'Id', 'Ins']).to_csv('Output/' + course.title + '.csv')


def apply_adjustment_ins(to_be_scheduled_lesson, date, ins_list):
    cur_lesson_df = to_be_scheduled_lesson.lesson_df[
        to_be_scheduled_lesson.lesson_df['Id'] == to_be_scheduled_lesson.id]
    for ins in ins_list:
            # point = to_be_scheduled_lesson.lesson_df.loc[to_be_scheduled_lesson.lesson_df.Id == to_be_scheduled_lesson.id, ins.name]
        adj = ins.get_adjustment(date=date)
        if cur_lesson_df.loc[:, ins.name].item() != 0:
            cur_lesson_df.loc[:, ins.name] += (adj + ins.cur_adjustment)
            # print('Adjustment for {} is {} + {} = {}'.format(ins.name, adj, ins.cur_adjustment, adj + ins.cur_adjustment))
            return cur_lesson_df
    return cur_lesson_df


# if an ins is scheduled for a lesson, all following lesson get -0.3 and all other ins get +0.1
def apply_adjustment_lesson(lesson, ins):
    for cur_ins in lesson.lesson_df.loc[lesson.lesson_df.Id == lesson.id].drop(['Title', 'Sequence', 'Order', 'Id'], axis=1):
        if cur_ins == ins.name:
            ins.apply_cur_adjustment(-0.5)
        elif lesson.lesson_df.loc[lesson.lesson_df.Id == lesson.id, cur_ins].item() != 0:
            ins.apply_cur_adjustment(0.2)

    # print(lesson.lesson_df)


def get_possible_lessons(course, cur_date):
    possible_lessons = []
    for l in course.lessons:
        if not l.scheduled:
            # Practice Class 01 corner case
            if l.code[0] == 1:
                if l.code[1] == 1 and not get_lesson(course=course, code=[1, 1]).scheduled:
                    possible_lessons.append(l)
                    break
                elif get_lesson(course=course, code=[1, 1]).scheduled:
                    possible_lessons.append(l)

            elif (l.week == 0 or (l.week == 1 and l.code[1] == 1)) and \
                    ((l.code[1] == 0 and get_lesson(course=course, code=[l.code[0] - 1, 1]).scheduled) or \
                    (l.code[1] > 1 and get_lesson(course=course, code=[l.code[0], l.code[1] - 1]).scheduled) or \
                    (l.code[1] == 1 and get_lesson(course=course, code=[l.code[0] - 1, 1]).scheduled)):
                possible_lessons.append(l)
            elif l.week == 1:
                pre_lesson = get_lesson(course=course, code=[l.code[0], l.code[1] - 1])
                if pre_lesson.scheduled and (cur_date - pre_lesson.date).days >= 3:
                    possible_lessons.append(l)
                if len(possible_lessons) == 0 and pre_lesson.scheduled:
                    possible_lessons.append(l)
    return possible_lessons

