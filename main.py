from main_schedule import main_schedule
from parse import *

class_input = 'Input/class_input_for_RL finished.csv'
ins_adjustment_input = 'Input/Ins.csv'


def main():

    # create lessons ob
    lesson_df = pd.read_csv(class_input).fillna(0)

    # create job ob
    ins_list = parse_ins(lesson_df, ins_df=pd.read_csv(ins_adjustment_input).fillna(0))

    testDate1 = date(2018, 9, 19)
    Fall2 = date(2018, 10, 28)
    testDate3 = date(2018, 8, 11)
    schedule_from = date(2018, 11, 5)

    Fall1 = Course(title='Fall01', start_date=testDate1, weekdys=13567,
                    lessons=parse_lesson(lesson_df), ins=ins_list, unavailable_ins = ['Jin'])
    Fall2 = Course(title='Fall02', start_date=Fall2, weekdys=24567,
                     lessons=parse_lesson(lesson_df), ins=ins_list, unavailable_ins = ['Jin'])
    course3 = Course(title='Summer03', start_date=testDate3, weekdys=24567,
                     lessons=parse_lesson(lesson_df), ins=ins_list, unavailable_ins = ['Joe'])
    course1 = Course(title='Summer01', start_date=date(2018, 5, 26), weekdys=24567,
                     lessons=parse_lesson(lesson_df), ins=ins_list, unavailable_ins = [])
    opt_level = 4
    schedule_week = 1
    scale_factor = 0.5
    main_schedule(courses=[Fall1, Fall2], start_date=schedule_from, opt_level=opt_level, schedule_week=schedule_week, scale_factor=scale_factor)


start = datetime.datetime.now()
main()
print('dur = {}'.format(datetime.datetime.now() - start))
quit(12)


def graph():
    # create lessons ob
    lesson_df = pd.read_csv(class_input).fillna(0)
    res = []
    levels = [3]
    for level in levels:
        scale_factor = 0
        while scale_factor <= 0:
            ins_list = parse_ins(lesson_df, ins_df=pd.read_csv(ins_adjustment_input).fillna(0))
            print('scale_factor = {}'.format(scale_factor))
            print('level = {}'.format(level))
            course3 = Course(title='Summer03', start_date=date(2018, 8, 11), weekdys=24567,
                             lessons=parse_lesson(lesson_df), ins=ins_list, unavailable_ins=['Joe'])
            Fall1 = Course(title='Fall01', start_date=date(2018, 9, 19), weekdys=13567,
                           lessons=parse_lesson(lesson_df), ins=ins_list, unavailable_ins=['Jin'])
            start = datetime.datetime.now()
            point, counter, point_list = main_schedule(courses=[course3,Fall1], start_date=date(2018, 10, 15), opt_level=level,
                          schedule_week=-1, scale_factor=scale_factor)
            dur = datetime.datetime.now() - start

            print('dur = {}'.format(dur))
            print('point = {}'.format(point_list))
            res.append([scale_factor, level, point, counter, dur, str(point_list)])
            scale_factor += 0.2
        #pd.DataFrame(res, columns=['scale_factor', 'level', 'point', 'counter', 'dur', 'point_list']).to_csv('Output/graph01.csv', mode = 'a', header=False)





