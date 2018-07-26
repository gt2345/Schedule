from lesson import Lesson
import pandas as pd

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




# Check if a lesson has Prerequisite.
# Return true if a lesson does not have prerequisite, or prerequisite lesson has been scheduled
def check_pre(lesson, course):
    pre = get_lesson(title=lesson.lessonDf[lesson.lessonDf['Title'].isin([lesson.title])]['Prerequisite'].item(), course=course)
    if pre == None or pre.scheduled == True:
        return True
    return False


def parse_input(classDf):
    lessons = []
    for title in classDf['Title']:
        # l = Lesson(title=title, lessonDf=classDf[classDf['Title'].isin([title])])
        l = Lesson(title=title, lessonDf=classDf,
                   code=[classDf[classDf['Title'].isin([title])]['Sequence'].item(),classDf[classDf['Title'].isin([title])]['Order'].item()])
        lessons.append(l)
    return lessons


# Return [lesson, points]
def get_optimal_and_update(possible_lessons, calendar_dict, date):
    max_point = -1
    opt_lesson = None
    opt_ins = None
    for l in possible_lessons:
        ins = l.get_ins(calendar_dict=calendar_dict, date=date, unavailableIns=[])
        point = 0
        if str(ins) != 'nan':
            point = l.lessonDf[l.lessonDf['Title'].isin([l.title])][ins].item()

        if point > max_point:
            max_point = point
            opt_ins = ins
            opt_lesson = l
    return [opt_lesson, opt_ins, max_point]