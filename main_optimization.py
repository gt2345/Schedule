from schedule_helper import *
from parse import *
from itertools import permutations
import copy
pre_scheduled_input = 'pre_scheduled.csv'


def optimization(opt_level, cur, courses, calendar_dict):
    all_courses_permu = list(permutations(courses))
    opt_schedule = []
    tmpx = 0
    while tmpx < opt_level:
        opt_schedule.append(Schedule(date=cur + datetime.timedelta(days=tmpx)))
        tmpx += 1

    pre_scheduled = pd.read_csv(pre_scheduled_input)
    #if not pre_scheduled.empty:
        # not pre_scheduled[pre_scheduled['Date'].isin([str(cur), str(second_day)])].empty:
        #drop_course = parse_pre_scheduled(courses=courses, pre_scheduled=pre_scheduled, opt_schedule=opt_schedule,
        #                                  calendar_dict=calendar_dict, cur=cur, second_day=second_day)
    opt_schedule_list = {}

    #for course_list in all_courses_permu:
    cur_schedule = []
    course = courses[0]
    lesson_dfs(opt_schedule_list=opt_schedule_list, opt_level=opt_level, opt_point=[0], cur_level=0,
                        cur_schedule=cur_schedule, courses=courses, cur_date=cur, calendar_dict=calendar_dict)
    return opt_schedule_list


def lesson_dfs(opt_schedule_list, opt_level, opt_point, cur_level, cur_schedule, courses, cur_date, calendar_dict):
    print('cur date in lesson dfs {}'.format(cur_date))
    if cur_level == opt_level:
        if opt_schedule_list is None:
            for cu in cur_schedule:
                opt_schedule_list[cu.date] = cu.make_copy(calendar_dict=calendar_dict)
        cur_point = 0
        print('cur schedule {}'.format(cur_schedule))
        for cu in cur_schedule:
            print('here cu  {}'.format(cu))
            if cu is not None:
                cur_point += cu.point
        print('cur point is {}     opt point is {}'.format(cur_point, opt_point[0]))
        if cur_point - 1 > opt_point[0]:
            opt_point[0] = cur_point
            for cu in cur_schedule:
                opt_schedule_list[cu.date] = cu.make_copy(calendar_dict=calendar_dict)
        return
    cur_date_schedule = Schedule(date=cur_date)
    for course in courses:
        print(cur_level)
        if (course.class_scheduled < course.class_total + 1 or course.practice_scheduled < course.practice_total) \
                and course.iter.has_lesson(date=cur_date):
            possible_lessons = get_possible_lessons(course=course, cur_date=cur_date)
            if len(possible_lessons) == 0:
                return

            for pl in possible_lessons:
                ins, point = get_ins(lesson=pl, course=course, calendar_dict=calendar_dict, date=cur_date,
                                     unavailable_ins=copy.deepcopy(course.unavailable_ins))
                #cur_date_schedule.add_course(course=course, lesson=pl, ins=ins, point=point, calendar_dict=calendar_dict)
                #course_dfs(cur_date_schedule)
                cur_schedule.append(cur_date_schedule)

                # handle end corner case
                if len(possible_lessons) == 1 and \
                                        course.class_scheduled + course.practice_scheduled + len(cur_schedule) == 1 + course.class_total + course.practice_total:
                    cur_level = opt_level - 1

                lesson_dfs(opt_schedule_list=opt_schedule_list, opt_level=opt_level, opt_point=opt_point,
                                    cur_level=cur_level + 1, cur_schedule=cur_schedule, courses=courses,
                                    cur_date=cur_date + datetime.timedelta(days=1), calendar_dict=calendar_dict)
                cur_schedule[-1].remove_course(course=course, lesson=pl, calendar_dict=calendar_dict)
                if not cur_schedule[-1].is_valid():
                    del cur_schedule[-1]
        else:
            lesson_dfs(opt_schedule_list=opt_schedule_list, opt_level=opt_level, opt_point=opt_point,
                       cur_level=cur_level + 1, cur_schedule=cur_schedule, courses=courses,
                       cur_date=cur_date + datetime.timedelta(days=1), calendar_dict=calendar_dict)


def course_dfs(cur_date_schedule, courses, level):
    pass

