import pandas as pd
from ins import Ins


# Get a Lesson object by title, if title is not valid, return None
def get_lesson(course, title=None, code=None, id=None):
    if title is None and code is None and id is None:
        return None

    if id is not None:
        for l in course.lessons:
            if l.id == id:
                return l

    if title is not None:
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


def generate_history(course):
    history = []
    for l in course.class_list:
        history.append([l.date, course.title, l.number, l.id, l.title, l.ins])
    pd.DataFrame(history, columns=['Date', 'Course', 'Number', 'Id', 'Title', 'Ins']).to_csv('Output/' + course.title + '.csv')


# if an ins is scheduled for a lesson, all following lesson get Ins.neg_adj and all other ins get Ins.pos_adj
def apply_adjustment_to_ins(course, ins):
    ins.update_cur_adjustment(Ins.neg_adj)
    for cur_ins in course.ins:
        if cur_ins != ins and cur_ins.cur_adjustment < 0:
            cur_ins.update_cur_adjustment(Ins.pos_adj)


def earliest_course_start_date(courses):
    start_dates = []
    for course in courses:
        start_dates.append(course.start_date)
    return min(start_dates)


def check_complete(courses):
    print('in check complete')
    for c in courses:
        print(c.class_scheduled)
        print(c.class_total + 1)
        print(c.practice_scheduled)
        print(c.practice_total)
        if c.class_scheduled < c.class_total + 1 or c.practice_scheduled < c.practice_total:
            return False
    return True


def apply_adjustment_from_ins(to_be_scheduled_lesson, date, course, calendar_dict):
    cur_lesson_df = to_be_scheduled_lesson.lesson_df[
        to_be_scheduled_lesson.lesson_df['Id'] == to_be_scheduled_lesson.id]
    for ins in course.ins:
        adj = ins.get_adjustment(date=date, calendar_dict=calendar_dict)
        if cur_lesson_df.loc[:, ins.name].item() != 0:
            cur_lesson_df.loc[:, ins.name] += (adj + ins.cur_adjustment)
    return cur_lesson_df


def get_ins_list(ins_list, ins_array):
    res_ins_list = []
    for ins in ins_list:
        if not ins.name in ins_array:
            res_ins_list.append(ins)
    return res_ins_list