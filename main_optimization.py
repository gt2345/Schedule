from parse import *
import copy
from itertools import permutations
pre_scheduled_input = 'pre_scheduled.csv'

CUR_COMPLETE = 0
COMPLETED = 0


def optimization(opt_level, cur, courses, calendar_dict, scale_factor, num_level):
    # get pre-scheduled lessons
    ret_opt_schedule_list = {}
    pre_scheduled = pd.read_csv(pre_scheduled_input)
    drop_course = parse_pre_scheduled(courses=courses, pre_scheduled=pre_scheduled,ret_opt_schedule_list=ret_opt_schedule_list,
                                          calendar_dict=calendar_dict, cur=cur, opt_level=opt_level)
    cur_schedule = []
    opt_point = [0]
    opt_point_x = 0
    opt_schedule_list = {}

    course_list_permu = list(permutations(courses))
    for course_list in course_list_permu:
        # TODO: remove one course for one day

        cur_data_opt_point = [0] * opt_level
        day_dfs(opt_schedule_list=opt_schedule_list, opt_level=opt_level, opt_point=opt_point, cur_level=0,
                cur_schedule=cur_schedule, courses=course_list, cur_date=cur, calendar_dict=calendar_dict,
                scale_factor=scale_factor, complete=[1 / (num_level * len(course_list_permu))])
        if opt_point[0] > opt_point_x:
            opt_point_x = opt_point[0]
            for osl in opt_schedule_list:
                if osl not in ret_opt_schedule_list:
                    ret_opt_schedule_list[osl] = opt_schedule_list[osl]
                else:
                    ret_opt_schedule_list[osl].update(opt_schedule_list[osl])

    print('After pruning left with = {}'.format(COMPLETED))
    return ret_opt_schedule_list


# use cur_date_schedule_res to store different course schedule for the same day
def course_dfs(cur_schedule, cur_date_schedule, courses, course_index, cur_date, calendar_dict, opt_schedule_list,
               opt_level, opt_point, cur_level, cur_data_opt_point, scale_factor, complete):

    if course_index == len(courses):
        # cur_date_schedule_res.append(cur_date_schedule.make_copy(calendar_dict=calendar_dict))
        # print('cur point {}'.format(cur_date_schedule.point))
        if cur_date_schedule.point > cur_data_opt_point[cur_level]:
            # print('at level = {} set cur date opt point by {} > {}'.format(cur_level, cur_date_schedule.point, cur_data_opt_point[cur_level]))
            cur_data_opt_point[cur_level] = cur_date_schedule.point

        elif cur_date_schedule.point < len(cur_date_schedule.schedule) * 5 or \
            cur_date_schedule.point < cur_data_opt_point[cur_level] - (opt_level - cur_level) * scale_factor:
            #print('pruning at level {}  {} , {} {}'.format(cur_level, courses, cur_data_opt_point, cur_date_schedule))
            global CUR_COMPLETE
            CUR_COMPLETE += complete[0]
            print('pruning = {}'.format(CUR_COMPLETE))
            return

        cur_schedule.append(cur_date_schedule)
        day_dfs(opt_schedule_list=opt_schedule_list, opt_level=opt_level, opt_point=opt_point,
                   cur_level=cur_level+1, cur_schedule=cur_schedule, courses=courses,
                   cur_date=cur_date + datetime.timedelta(days=1), calendar_dict=calendar_dict,
                scale_factor=scale_factor, complete=complete)
        del cur_schedule[-1]
        return

    course = courses[course_index]
    if (course.class_scheduled < course.class_total + 1 or course.practice_scheduled < course.practice_total) \
            and course.has_lesson(date=cur_date):
        possible_lessons = get_possible_lessons(course=course, cur_date=cur_date)
        print("At Date = {} {}".format(cur_date, possible_lessons))
        if len(possible_lessons) == 0:
            if course.all_scheduled():
                course_dfs(cur_schedule=cur_schedule, cur_date_schedule=cur_date_schedule, courses=courses,
                           course_index=course_index + 1, cur_date=cur_date, calendar_dict=calendar_dict,
                           cur_level=cur_level,
                           opt_level=opt_level, opt_point=opt_point, opt_schedule_list=opt_schedule_list,
                           cur_data_opt_point=cur_data_opt_point, scale_factor=scale_factor, complete=complete)
            else:
                print('return for not able to schedule')
                return
        for pl in possible_lessons:
            ins, point = get_ins(lesson=pl, course=course, calendar_dict=calendar_dict, date=cur_date,
                                 unavailable_ins=copy.deepcopy(course.unavailable_ins))
            print("ins = {} point = {}".format(ins, point))
            cur_date_schedule.add_course(course=course, lesson=pl, ins=ins, point=point, calendar_dict=calendar_dict)
            course_dfs(cur_schedule=cur_schedule, cur_date_schedule=cur_date_schedule, courses=courses,
                       course_index=course_index+1, cur_date=cur_date, calendar_dict=calendar_dict, cur_level=cur_level,
                       opt_level=opt_level, opt_point=opt_point, opt_schedule_list=opt_schedule_list,
                       cur_data_opt_point=cur_data_opt_point, scale_factor=scale_factor, complete=[complete[0]/len(possible_lessons)])
            cur_date_schedule.remove_course(course=course, lesson=pl, calendar_dict=calendar_dict)
    else:
        course_dfs(cur_schedule=cur_schedule, cur_date_schedule=cur_date_schedule, courses=courses,
                   course_index=course_index + 1, cur_date=cur_date, calendar_dict=calendar_dict, cur_level=cur_level,
                   opt_level=opt_level, opt_point=opt_point, opt_schedule_list=opt_schedule_list,
                   cur_data_opt_point=cur_data_opt_point, scale_factor=scale_factor, complete=complete)


def day_dfs(opt_schedule_list, opt_level, opt_point, cur_level, cur_schedule, courses, cur_date, calendar_dict, scale_factor, complete):
    if cur_level == opt_level:
        global CUR_COMPLETE
        global COMPLETED
        CUR_COMPLETE += complete[0]
        COMPLETED += complete[0]
        print('percentage = {}'.format(CUR_COMPLETE))
        if len(opt_schedule_list) == 0:
            for cu in cur_schedule:
                opt_schedule_list[cu.date] = cu.make_copy(calendar_dict=calendar_dict)
        cur_point = 0

        for cu in cur_schedule:
            if cu is not None:
                cur_point += cu.point
        #print('{} cur schedule {}'.format(cur_point, cur_schedule))
        if cur_point > opt_point[0]:
            opt_point[0] = cur_point
            for cu in cur_schedule:
                opt_schedule_list[cu.date] = cu.make_copy(calendar_dict=calendar_dict)
            #print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   here update opt_schedule_list')

        return

    cur_date_schedule = Schedule(date=cur_date)
    cur_data_opt_point = [0] * opt_level
    course_dfs(cur_schedule=cur_schedule, cur_date_schedule=cur_date_schedule, courses=courses,
               course_index=0, cur_date=cur_date, calendar_dict=calendar_dict, opt_schedule_list=opt_schedule_list,
               cur_level=cur_level, opt_level=opt_level, opt_point=opt_point, cur_data_opt_point=cur_data_opt_point,
               scale_factor=scale_factor, complete=complete)
