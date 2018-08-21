from course import Course
from schedule import Schedule
from schedule_helper_basic import *
import datetime


# Return [course, lesson, ins, points]
def get_optimal_for_one_course(course, possible_lessons, calendar_dict, date):
    max_point = -1
    opt_lesson = None
    opt_ins = None
    for l in possible_lessons:
        get_ins_ret = get_ins(lesson=l, course=course, calendar_dict=calendar_dict, date=date, unavailable_ins=[])
        ins = get_ins_ret[0]
        point = get_ins_ret[1]
        if point > max_point:
            max_point = point
            opt_ins = ins
            opt_lesson = l
    if max_point <= 0:
        opt_ins = None
    return [course, opt_lesson, opt_ins, max_point]


# return [ins, point]
def get_ins(lesson, course, calendar_dict, date, unavailable_ins):
    drop_list = ['Title', 'Sequence', 'Order', 'Id', 'Week'] + unavailable_ins
    cur_lesson_df = apply_adjustment_from_ins(course=course, to_be_scheduled_lesson=lesson, date=date)
    # print(cur_lesson_df)
    cur_lesson_df = cur_lesson_df.drop(drop_list, axis=1)
    ins_name = cur_lesson_df.idxmax(axis=1).item()
    ins = get_ins_by_name(course=course, name=ins_name)
    if date not in calendar_dict:
        calendar_dict[date] = []
    # ins is not scheduled for today or yesterday
    while ins is None or (ins.name in calendar_dict[date]) or \
             (date - datetime.timedelta(days=1) in calendar_dict and ins.name in calendar_dict[date - datetime.timedelta(days=1)]):
        unavailable_ins.append(ins_name)
        ins = get_ins(lesson=lesson, course=course, unavailable_ins=unavailable_ins, calendar_dict=calendar_dict, date=date)[0]
    return [ins, cur_lesson_df[ins.name].item()]


def get_possible_lessons_detail(course, cur_date, consider_week):
    possible_lessons = []
    for l in course.lessons:
        if not l.is_scheduled():
            # Practice Class 01 corner case
            if l.code[0] == 1:
                if l.code[1] == 1 and not get_lesson(course=course, code=[1, 1]).is_scheduled():
                    possible_lessons.append(l)
                    break
                elif get_lesson(course=course, code=[1, 1]).is_scheduled():
                    possible_lessons.append(l)

            elif (l.week == 0 or (l.week == 1 and l.code[1] == 1)) and \
                    ((l.code[1] == 0 and get_lesson(course=course, code=[l.code[0] - 1, 1]).is_scheduled()) or \
                    (l.code[1] > 1 and get_lesson(course=course, code=[l.code[0], l.code[1] - 1]).is_scheduled()) or \
                    (l.code[1] == 1 and get_lesson(course=course, code=[l.code[0] - 1, 1]).is_scheduled())):
                possible_lessons.append(l)
            elif l.week == 1:
                if l.code[1] > 1:
                    pre_lesson = get_lesson(course=course, code=[l.code[0], l.code[1] - 1])
                else:
                    pre_lesson = get_lesson(course=course, code=[l.code[0] - 1, 1])

                if pre_lesson.is_scheduled():
                    if consider_week is False or (cur_date - pre_lesson.get_date()).days >= Course.week_separator:
                        possible_lessons.append(l)
    return possible_lessons


# first time separate week attribute lessons be week_separator
# if no available lessons, disregard week_separator
def get_possible_lessons(course, cur_date):
    possible_lessons = get_possible_lessons_detail(course=course, cur_date=cur_date, consider_week=True)
    if len(possible_lessons) == 0 or (len(possible_lessons) == 1 and possible_lessons[0].week == 0):
        possible_lessons = get_possible_lessons_detail(course=course, cur_date=cur_date, consider_week=False)
    return possible_lessons


# courses = [course1, course2, course3]
# return optimal schedule for one particular course order of one day
def get_one_schedule(courses, cur_date, calendar_dict, drop_list, drop_lesson):
    cur_schedule = Schedule(cur_date)
    for c in courses:
        # print('{} at {}'.format(c.title, c.iter.peek()))
        if cur_date > c.iter.peek():
            lesson_date = c.iter.peek_second()
        else:
            lesson_date = c.iter.peek()
        if c.title in drop_list:
            print('course dropped')
            continue
        # print('this lesson date {}'.format(lesson_date))
        if (c.class_scheduled < c.class_total + 1 or c.practice_scheduled < c.practice_total) \
                and lesson_date == cur_date:
            possible_lessons = get_possible_lessons(course=c, cur_date=cur_date)
            # print('today {}  before update  {}'.format(cur_date, possible_lessons))
            if drop_lesson is not None and len(possible_lessons) > 1:

                for d in drop_lesson:
                    # print('here {} {}'.format(len(drop_lesson), d))
                    if d.is_valid() and d.date == cur_date:
                        d.update_possible_lessons(course=c, possible_lessons=possible_lessons)
                        # print('today {}  after update  {}'.format(cur_date, possible_lessons))
            if len(possible_lessons) == 0:
                if c.class_total + 1 - c.class_scheduled == 1 or c.practice_total - c.practice_scheduled == 1:
                    continue
                else:
                    print(cur_date)
                    print(c.title)
                    print(c.class_scheduled)
                    print(c.class_total)
                    print(c.practice_scheduled)
                    print(c.practice_total)
                    print('Not Able to Schedule')
                    quit(99)
            else:
                optimal_for_one_course = get_optimal_for_one_course(course=c, possible_lessons=possible_lessons,
                                                    calendar_dict=calendar_dict, date=cur_date)
                cur_schedule.add_course(course=c, lesson=optimal_for_one_course[Schedule.lesson_index],
                                        ins=optimal_for_one_course[Schedule.ins_index],
                                        point=optimal_for_one_course[-1],calendar_dict=calendar_dict)
    # cur_schedule.clean_up(calendar_dict=calendar_dict)
    print('cur schedule {}'.format(cur_schedule))
    return cur_schedule


