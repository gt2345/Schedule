from main_optimization_modified_for_RL import *
from parse import *


class_input = 'Input/test_class_input_for_RL.csv'
ins_adjustment_input = 'Input/Ins.csv'
truth = 'Output/history.csv'
start_date = date(2018, 6, 30)
end_date = date(2018, 9, 22)
testDate3 = date(2018, 8, 11)
lesson_df = pd.read_csv(class_input).fillna(0)
ins_list = parse_ins(lesson_df, ins_df=pd.read_csv(ins_adjustment_input).fillna(0))
course2 = Course(title='Summer02', start_date=date(2018, 6, 30), weekdys=13567,
                 lessons=parse_lesson(lesson_df), ins=get_ins_list(ins_list=ins_list, ins_array=["Jin"]),
                 unavailable_ins = ["Jin"])
course1 = Course(title='Summer01', start_date=date(2018, 5, 26), weekdys=24567,
                 lessons=parse_lesson(lesson_df), ins=get_ins_list(ins_list=ins_list, ins_array=['Joe']),
                 unavailable_ins = ['Joe'])
course3 = Course(title='Summer03', start_date=testDate3, weekdys=24567,
                         lessons=parse_lesson(lesson_df), ins=get_ins_list(ins_list=ins_list, ins_array=['Joe']),
                         unavailable_ins=['Joe'])
courses = [course1, course2, course3]
truth_df = pd.read_csv(truth).fillna(0)
summer1_truth = pd.read_csv("Summer01_history_final.csv").fillna(0)
summer2_truth = pd.read_csv("Summer02_history_final.csv").fillna(0)
summer3_truth = pd.read_csv("Summer03_history_final.csv").fillna(0)
history = {course1:summer1_truth, course2:summer2_truth, course3:summer3_truth}


def get_course_by_title(courses, title):
    for c in courses:
        if c.title == title:
            return c
    return None


def get_lesson_from_schedule(schedule):
    res = []
    for s in schedule.schedule:
        res.append(s[Schedule.lesson_index])
    return res


def get_max_per_week():
    test_start = date(2018,6,30)
    test_end = date(2018,9,21)
    cur = test_start
    history = [summer1_truth, summer2_truth, summer3_truth]
    res = {}
    counter = 0

    for history_df in history:
        for index, row in history_df.iterrows():
            if '/' in row['Date']:
                cur_date_month, cur_date_day, cur_date_year = row['Date'].split('/')
            else:
                cur_date_year, cur_date_month, cur_date_day = row['Date'].split('-')
            history_df.loc[index, 'Date'] = date(int(cur_date_year), int(cur_date_month), int(cur_date_day))
    while cur < test_end:
        counter += 1
        cur_round = cur
        res_temp = {}
        for x in range(7):
            for history_df in history:
                # print(history_df[history_df["Date"] == cur_round])
                if history_df[history_df["Date"] == cur_round]["Ins"].empty:
                    continue
                ins = get_ins_by_name(course=course2, name=history_df[history_df["Date"] == cur_round]["Ins"].item())
                if ins is not None:
                    if ins.name not in res_temp:
                        res_temp[ins.name] = 0
                    res_temp[ins.name] += 1
            cur_round += datetime.timedelta(days=1)
            for tmp in res_temp:
                if tmp not in res or res_temp[tmp] > res[tmp]:
                    res[tmp] = res_temp[tmp]
                    print("{}   {}".format(cur, tmp))
        cur += datetime.timedelta(days=1)
    print(counter)
    print(res)


def main():

    for history_df in history.values():
        for index, row in history_df.iterrows():
            if '/' in row['Date']:
                cur_date_month, cur_date_day, cur_date_year = row['Date'].split('/')
            else:
                cur_date_year, cur_date_month, cur_date_day = row['Date'].split('-')
            history_df.loc[index, 'Date'] = date(int(cur_date_year), int(cur_date_month), int(cur_date_day))
    scheduled = main_schedule(courses=courses, start_date=start_date, opt_level=1, schedule_week=1, scale_factor=3)
    quit(44)
    #scheduled = scheduled.fillna(0)
    # print(scheduled)
    for index, row in summer2_truth.iterrows():
        year, month, day = row["Date"].split("-")
        cur_date = date(int(year), int(month), int(day))
        summer2_truth.loc[index, 'Date'] = cur_date

        if start_date <= cur_date <= end_date:
            print(cur_date)
            if row["Course_y"] != 0:
                scheduled_lesson = get_lesson(course=course1, title=row['Class_y'])
                print(scheduled_lesson)


def main_schedule(courses, start_date, opt_level, schedule_week, scale_factor):
    start = datetime.datetime.now()
    calendar_dict = {}
    point = 0
    counter = 0
    all = 0
    correct = 0
    point_list = []
    # Schedule start after course start date
    if earliest_course_start_date(courses) < start_date:
        parse_scheduled(courses=courses, start_date=start_date,
                        course_start_date=earliest_course_start_date(courses), calendar_dict=calendar_dict)

    cur = start_date
    num_level = get_percentage_scale(schedule_week=schedule_week, opt_level=opt_level, courses=courses)

    while True:
        print(cur)

        opt_schedule_list = []
        if cur >= end_date:
            break
        # print('Today date {}'.format(cur))
        # for one day, schedule with different order
        opt_schedule_list_q = optimization(opt_level=opt_level, cur=cur, courses=courses, calendar_dict=calendar_dict,
                                         scale_factor=scale_factor,
                                         num_level = num_level)
        while not opt_schedule_list_q.empty():
            opt_schedule_list.append(opt_schedule_list_q.get())


        opt_schedule_list.reverse()
        # process opt schedule list
        for tmp in opt_schedule_list:
            print(tmp)
            point += tmp.point
            point_list.append(tmp.point)
            counter += len(tmp.schedule)
        if len(opt_schedule_list) == 0:
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% not able to schedule %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            break

        #
        truth_schedule = Schedule(date=cur)
        ins_name = ""
        for c in courses:
            c_df = history[c]

            if not c_df[c_df["Date"] == cur]["Id"].empty:
                truth_lesson = get_lesson(course=c, id=c_df[c_df["Date"] == cur]["Id"].item())
                truth_ins = get_ins_by_name(course=c, name=c_df[c_df["Date"] == cur]["Ins"].item())
                print("truth lesson {}".format(truth_lesson))
                print("truth ins {}".format(truth_ins.name))
                if c.title == "Summer02":
                    ins_name = truth_ins.name
                    if ins_name == "Joe":
                        print(truth_ins.get_adjustment(date=cur, calendar_dict=calendar_dict))

                truth_schedule.add_course(course=c,lesson=truth_lesson,ins=truth_ins,point=0,calendar_dict=calendar_dict)

        if course2.has_lesson(date=cur):
            all += 1
            if truth_schedule.is_in(list_of_schedule=opt_schedule_list, course=course2):
                print("-- - - - - - - - - - - - - - - - - - - - - - --------------------------------")
                correct += 1
            #elif ins_name != "Sun" and ins_name != "Yan" and cur != date(2018,9,3) and cur != date(2018,8,1) and cur != date(2018,9,14) and cur != date(2018,7,1) :
                            #cur != date(2018,7,8) and cur != date(2018,8,17):
             #               cur != date(2018,9,3) and cur != date(2018,8,3) \
             #       and cur != date(2018,7,11) and cur != date(2018,7,18)  \
             #       and cur != date(2018,8,22) and cur != date(2018,9,17):
            #else:
                #quit(11)
        #opt_schedule_list[0].update(truth_schedule)
        opt_schedule_list[0].schedule_today(calendar_dict=calendar_dict)

        if cur.year > 2018 or check_complete(courses=courses):
            break
        else:
            cur += datetime.timedelta(days=opt_level)

    print("all = {}".format(all))
    print("correct = {}".format(correct))
    # generate calendar to use for csv
    calendar_df = pd.DataFrame()
    for c in courses:
        calendar_list = []
        for l in c.class_list:
            calendar_list.append([l.date, c.title, l.number, l.title, l.ins])
        if calendar_df.empty:
            calendar_df = pd.DataFrame(calendar_list, columns=['Date', 'Course', 'Number', 'Class', 'Ins'])
        else:
            calendar_df = pd.merge(calendar_df,
                                   pd.DataFrame(calendar_list,columns=['Date', 'Course', 'Number', 'Class', 'Ins']),
                                   how='outer', on='Date', sort='Date')
    #print('point: {}'.format(point))
    #print('counter: {}'.format(counter))
    print('dur = {}'.format(datetime.datetime.now() - start))
    return calendar_df


main()


