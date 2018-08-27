from schedule_helper_basic import *


class Schedule:

    course_index = 0
    lesson_index = 1
    ins_index = 2
    point_index = 3

    def __init__(self, date):
        self.schedule = []
        self.date = date
        self.point = 0

    def add_course(self, course, lesson, ins, point, calendar_dict):
        self.schedule.append([course, lesson, ins, point])
        self.point += point
        if ins is not None:
            if self.date not in calendar_dict:
                calendar_dict[self.date] = []
            calendar_dict[self.date].append(ins.name)
        lesson.temp_date = self.date
        lesson.schedule_buffer = True

    def remove_course(self, course, lesson, calendar_dict):
        for idx, val in enumerate(self.schedule):
            if val[Schedule.course_index] == course and val[Schedule.lesson_index].title == lesson.title:
                if val[Schedule.ins_index] is not None:
                    calendar_dict[self.date].remove(val[Schedule.ins_index].name)
                    self.point -= val[Schedule.point_index]
                val[Schedule.lesson_index].temp_date = None
                val[Schedule.lesson_index].schedule_buffer = False
                del self.schedule[idx]

    def schedule_today(self, calendar_dict):
        calendar_dict[self.date] = []
        for s in self.schedule:
            s[Schedule.course_index].schedule(lesson=s[Schedule.lesson_index], date=self.date, ins=s[Schedule.ins_index])
            s[Schedule.course_index].clear_schedule_buffer()
            if s[Schedule.ins_index] is not None:
                calendar_dict[self.date].append(s[Schedule.ins_index].name)
                apply_adjustment_to_ins(course=s[Schedule.course_index], ins=s[Schedule.ins_index])
        # self.schedule = []

    def clean_up(self, calendar_dict):
        calendar_dict[self.date] = []
        for s in self.schedule:
            lesson = s[Schedule.lesson_index]
            lesson.temp_date = None
            lesson.schedule_buffer = False

    def __str__(self):
        return '############## {}    {} '.format(self.date, self.schedule)

    def __repr__(self):
        return '{} {}'.format(self.date, self.schedule)

    def is_valid(self):
        return len(self.schedule) > 0

    def better_than(self, other):
        if self.is_valid() and other.is_valid():
            return self.point > other.point
        return self.is_valid()

    def update(self, other):
        if other.is_valid():
            for s in other.schedule:
                cur_course = s[Schedule.course_index]
                for t in self.schedule:
                    if t[Schedule.lesson_index].pre_scheduled is True:
                        continue
                    if t[Schedule.course_index] == cur_course:
                        self.point -= t[Schedule.point_index]
                        self.schedule.remove(t)
                self.schedule.append(s)
                self.point += s[Schedule.point_index]

    def update_possible_lessons(self, possible_lessons, course):
        for s in self.schedule:
            if course == s[Schedule.course_index] and s[Schedule.lesson_index] in possible_lessons:
                possible_lessons.remove(s[Schedule.lesson_index])

    # make a copy with same course and lesson reference
    def make_copy(self, calendar_dict):
        copy = Schedule(date=self.date)

        for k in self.schedule:
            if k[Schedule.ins_index] is not None:
                calendar_dict[self.date].remove(k[Schedule.ins_index].name)
            copy.add_course(course=k[Schedule.course_index], lesson=k[Schedule.lesson_index],
                           ins=k[Schedule.ins_index], point=k[Schedule.point_index], calendar_dict=calendar_dict)
        return copy