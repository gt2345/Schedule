import pandas as pd
from ins import Ins
from course import Course


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
        history.append([l.date, l.number, l.title, l.ins, l.id, course.title])
    lessons_history = pd.DataFrame(history, columns=['Date', 'Number', 'Title', 'Ins', 'Id', 'Course'])
    lessons_history.to_csv('Output/' + course.title + '.csv', index=False)


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

    for c in courses:
        if c.class_scheduled < c.class_total + 1 or c.practice_scheduled < c.practice_total:
            return False
    return True


def apply_adjustment(to_be_scheduled_lesson, date, course, calendar_dict):
    cur_lesson_df = to_be_scheduled_lesson.lesson_df[
        to_be_scheduled_lesson.lesson_df['Id'] == to_be_scheduled_lesson.id]
    # apply adjustment from lessons
    counter = 0
    for l in course.lessons:

        #print(l.is_scheduled())
        if l == to_be_scheduled_lesson or l.id > Course.prefer_to_be_ordered_up_to:
            break
        if not l.is_scheduled():
            counter += 1
    # apply adjustment from ins
    for ins in course.ins:
        adj = ins.get_adjustment(date=date, calendar_dict=calendar_dict) - (counter * Course.not_scheduled_scale)
        if cur_lesson_df.loc[:, ins.name].item() != 0:
            cur_lesson_df.loc[:, ins.name] += (adj + ins.cur_adjustment)
    return cur_lesson_df


def get_ins_list(ins_list, ins_array):
    res_ins_list = []
    for ins in ins_list:
        if not ins.name in ins_array:
            res_ins_list.append(ins)
    return res_ins_list


def course_handler(courses):
    res = [courses]
    if len(courses) < 2:
        return res
    else:
        i = 0
        courses_x = []
        while i < len(courses) - 2:
            courses_x.append(courses[i])
            i += 1
        courses_x.append(courses[-1])
        courses_x.append(courses[-2])
    res.append(courses_x)
    return res