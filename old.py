rand = random.random()
if rand <= 0.5:
    l = c.lessons[0][c.class_scheduled]
    if check_pre(lesson=l, course=c):
        c.class_scheduled += 1
    else:
        l = c.lessons[1][c.practice_scheduled]
        if check_pre(lesson=l, course=c):
            c.practice_scheduled += 1
        else:
            print(l)
            print('Not Able to Schedule')
            quit(1)
else:
    l = c.lessons[1][c.practice_scheduled]
    if check_pre(lesson=l, course=c):
        c.practice_scheduled += 1
    else:
        l = c.lessons[0][c.class_scheduled]
        if check_pre(lesson=l, course=c):
            c.class_scheduled += 1
        else:
            print(l)
            print('Not Able to Schedule')
            quit(2)
elif c.class_scheduled < len(c.lessons[0]):
l = c.lessons[0][c.class_scheduled]
if check_pre(lesson=l, course=c):
    c.class_scheduled += 1
else:
    print(l)
    print('Not Able to Schedule')
    quit(3)
else:
l = c.lessons[1][c.practice_scheduled]
if check_pre(lesson=l, course=c):
    c.practice_scheduled += 1
else:
    print(l)
    print('Not Able to Schedule')
    quit(4)


insDf = pd.read_csv('Punch card - Ins.csv')
cur_lessonDf = testDf[testDf['Title'].isin(['Recursion I and Binary search'])].drop(['Title', 'Code'], axis=1)
print(cur_lessonDf)
# print(insDf)
for i in insDf['Ins']:
    # print(time.strftime(insDf[insDf['Ins'].isin([i])]['Start'].item()))
    if datetime(2018, 5, 25) >= datetime.strptime(str(insDf[insDf['Ins'].isin([i])]['Start'].item()), '%Y-%m-%d') \
            and datetime(2018, 5, 25) <= datetime.strptime(str(insDf[insDf['Ins'].isin([i])]['End'].item()), '%Y-%m-%d'):
        cur_lessonDf[i] += insDf[insDf['Ins'].isin([i])]['Effect'].item() * insDf[insDf['Ins'].isin([i])]['Point'].item()
        print('here {}'.format(cur_lessonDf[i].item()))
        print(cur_lessonDf)
        break

    def get_ins(self, calendar_dict, date, unavailableIns):
        # drop_list = ['Title', 'Prerequisite'] + unavailableIns
        drop_list = ['Title', 'Sequence', 'Order'] + unavailableIns

        # Update lessonDf with date
        # insDf = pd.read_csv('Punch card - Ins.csv')
        cur_lessonDf = self.lessonDf[self.lessonDf['Title'].isin([self.title])].drop(drop_list, axis=1)



        # ins = self.lessonDf[self.lessonDf['Title'].isin([self.title])].drop(drop_list, axis=1).idxmax(axis=1).item()
        ins = cur_lessonDf.idxmax(axis=1).item()

        if date not in calendar_dict:
            calendar_dict[date] = []

        while (ins in calendar_dict[date]) or \
                 (date - datetime.timedelta(days=1) in calendar_dict and ins in calendar_dict[date - datetime.timedelta(days=1)]):
            if str(ins) != 'nan':
                unavailableIns.append(ins)
            ins = self.get_ins(unavailableIns=unavailableIns, calendar_dict=calendar_dict, date=date)

        # print('At {} for class {} ins is {} '.format(date, self.title, ins))
        return ins


    if to_be_scheduled_lesson.lesson_df.loc[
                to_be_scheduled_lesson.lesson_df.Id == to_be_scheduled_lesson.id, ins.name].item() > 0:
        to_be_scheduled_lesson.lesson_df.loc[
            to_be_scheduled_lesson.lesson_df.Id == to_be_scheduled_lesson.id, ins.name] += adj
        print(to_be_scheduled_lesson.lesson_df[to_be_scheduled_lesson.lesson_df['Id'] == to_be_scheduled_lesson.id])

try:
    cur_lesson_info = classDf[classDf['Id'] == row['Id']]
    history_lesson = Lesson(id=row['Id'], title=cur_lesson_info['Title'].item(), lesson_df=classDf,
                            code=[cur_lesson_info['Sequence'].item(), cur_lesson_info['Order'].item()])
except:
    print(row)


def schedule(courses, start_date):
    # Schedule not from course start date
    for c in courses:

        if c.start_date < start_date and len(c.class_list) == 0:
            history = pd.read_csv(c.title + '_history_final.csv')
            parse_scheduled(history=history, course=c, startdate=start_date)
            c.reset_iter(start_date=start_date)

    all_courses_permu = permutations(courses)
    calendar_dict = {}
    cur = start_date

    while True:
        done = True

        for c in courses:
            if c.class_scheduled <= c.class_total and c.practice_scheduled <= c.practice_total:
                done = False
                if c.iter.peek() == cur:
                    possible_lessons = get_possible_lessons(course=c, cur_date=cur)
                    print(possible_lessons)
                    if len(possible_lessons) == 0:
                        print(cur)
                        print(c.title)
                        print('Not Able to Schedule')
                        for nl in c.class_list:
                            print(str(nl))
                        print('Class scheduled {}'.format(c.class_scheduled))
                        print('Class total {}'.format(c.class_total))
                        print('Practice scheduled {}'.format(c.practice_scheduled))
                        print('Practice total {}'.format(c.practice_total))
                        quit(99)
                    else:
                        opt_retval = get_optimal_and_update(course=c, possible_lessons=possible_lessons,
                                                            calendar_dict=calendar_dict, date=cur)
                        lesson = opt_retval[0]
                        ins = opt_retval[1]
                        if ins is not None:
                            calendar_dict[cur].append(ins.name)
                    c.schedule(lesson=lesson, date=cur, ins=ins)
                    c.iter.__next__()
        if done:
            break
        else:
            cur += datetime.timedelta(days=1)
    for c in courses:
        generate_history(course=c)
        for x in c.class_list:
            print(str(x))
    calendar_df = pd.DataFrame()
    for c in courses:
        calendar_list = []
        for l in c.class_list:
            calendar_list.append([l.date, c.title, l.number, l.title, l.ins])
        if calendar_df.empty:
            calendar_df = pd.DataFrame(calendar_list, columns=['Date', 'Course', 'Number', 'Class', 'Ins'])
        else:
            calendar_df = pd.merge(calendar_df,
                                   pd.DataFrame(calendar_list, columns=['Date', 'Course', 'Number', 'Class', 'Ins']),
                                   how='outer', on='Date', sort='Date')
    return calendar_df


# Return [lesson, ins, points]
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

    if opt_ins is not None:
        apply_adjustment_lesson(lesson=opt_lesson, ins=opt_ins)
        print('chosen lesson {}'.format(opt_lesson))
        print('chosen ins {}'.format(opt_ins))
        print('curent point is {}'.format(max_point))
    return [opt_lesson, opt_ins, max_point]

# Schedule not from course start date
for c in courses:
    if c.start_date < start_date and len(c.class_list) == 0:
        history = pd.read_csv(c.title + '_history_final.csv')
        parse_scheduled(history=history, course=c, startdate=start_date)
        c.reset_iter(start_date=start_date)

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

    for ins in ins_list:
        if ins.name == 'Tang':
            ins.set_adjustment('1234', -10)
        if ins.name == 'Lu':
            ins.set_adjustment('1', -20)
        if ins.name == "Jin":
            ins.set_adjustment('12347', -20)
        if ins.name == 'Zhao':
            ins.cur_adjustment_scale = 1.5
        if ins.name == 'Sun':
            ins.set_absent(absent_start=date(2018, 8, 20), absent_end=date(2018, 9, 20))

    while True:
        print('Today date {}'.format(cur))
        second_day = cur + datetime.timedelta(days=1)
        opt_schedule = []
        tmpx = 0
        while tmpx < opt_level:
            opt_schedule.append(Schedule(date=cur + datetime.timedelta(days=tmpx)))
            tmpx += 1
        # opt_schedule = [Schedule(date=cur), Schedule(date=second_day)]
        # if one lesson is pre-scheduled
        pre_scheduled = pd.read_csv(pre_scheduled_input)

        drop_course = []

        if not pre_scheduled.empty:
                #not pre_scheduled[pre_scheduled['Date'].isin([str(cur), str(second_day)])].empty:
            drop_course = parse_pre_scheduled(courses=courses, pre_scheduled=pre_scheduled, opt_schedule=opt_schedule,
                                              calendar_dict=calendar_dict, cur=cur, second_day=second_day)
        drop_course = []
        # for one day, schedule with different order
        for course_list in all_courses_permu:
            print(course_list)
            first_schedule_today = get_one_schedule(courses=course_list, cur_date=cur,
                                            calendar_dict=calendar_dict, drop_list=drop_course, drop_lesson = None)
            first_schedule_tomorrow = get_one_schedule(courses=course_list, cur_date=second_day,
                                                           calendar_dict=calendar_dict,
                                                       drop_list=drop_course, drop_lesson = None)
            first_schedule = [first_schedule_today, first_schedule_tomorrow]
            first_schedule_point = 0
            for one in first_schedule:
                first_schedule_point += one.point
                one.clean_up(calendar_dict=calendar_dict)


            print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')

            second_schedule_today = get_one_schedule(courses=course_list, cur_date=cur,
                                            calendar_dict=calendar_dict, drop_list=drop_course, drop_lesson=first_schedule)
            second_schedule_tomorrow = get_one_schedule(courses=course_list, cur_date=second_day,
                                                           calendar_dict=calendar_dict,
                                                        drop_list=drop_course, drop_lesson=None)
            second_schedule = [second_schedule_today, second_schedule_tomorrow]
            second_schedule_point = 0
            for one in second_schedule:
                second_schedule_point += one.point
                one.clean_up(calendar_dict=calendar_dict)

            if first_schedule_point >= second_schedule_point:
                first += 1
                for index, one in enumerate(opt_schedule):
                    one.update(first_schedule[index])
            else :
                second += 1
                for index, one in enumerate(opt_schedule):
                    one.update(second_schedule[index])
            print('first point {}'.format(first_schedule_point))
            print('second point {}'.format(second_schedule_point))
        for one in opt_schedule:
            if one.is_valid():
                print('Actually scheduled')
                print(opt_schedule)
                one.schedule_today(calendar_dict=calendar_dict)
        print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')

        if cur.year > 2018 or check_complete(courses=courses):
            break
        else:
            cur += datetime.timedelta(days=opt_level)
