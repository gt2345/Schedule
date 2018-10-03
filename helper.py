import pandas as pd
import datetime


def generate_history(course, start_date = None):
    date_list = []
    if start_date is not None:
        for i in range(7):
            date_list.append(start_date + datetime.timedelta(days=i))
    history = []
    calendar = pd.DataFrame(columns=date_list, index=[course.title, "Title", "Ins"])

    for l in course.class_list:
        history.append([l.date, l.number, l.title, l.ins, l.id, course.title])
        if start_date is not None:
            try:
                index = date_list.index(l.date)
            except ValueError:
                continue
            if l.practice:
                key = "Practice " + str(l.number)
            else:
                key = "Class " + str(l.number)
            calendar.loc[course.title, l.date] = key
            calendar.loc["Title", l.date] = l.title
            calendar.loc["Ins", l.date] = l.ins
    if start_date is not None:
        pd.DataFrame(calendar).to_csv("Output/test.csv", mode='a')
    lessons_history = pd.DataFrame(history, columns=['Date', 'Number', 'Title', 'Ins', 'Id', 'Course'])
    lessons_history.to_csv('Output/' + course.title + '.csv', index=False)


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


# not used anymore
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


def get_percentage_scale(schedule_week, opt_level, courses):
    if schedule_week > 0:
        if (7 * schedule_week) % opt_level == 0:
            return (7 * schedule_week) / opt_level
        return int((7 * schedule_week) / opt_level) + 1
    num_days_left = 0
    for c in courses:
        if (c.practice_total - c.practice_scheduled) + (c.class_total - c.class_scheduled + 1) > num_days_left:
            num_days_left = (c.practice_total - c.practice_scheduled) + (c.class_total - c.class_scheduled + 1)
    if (num_days_left * (7/5)) % opt_level == 0:
        return (num_days_left * (7/5)) / opt_level
    return int((num_days_left * (7/5)) / opt_level) + 1