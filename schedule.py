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

    def schedule_today(self, calendar_dict):
        calendar_dict[self.date] = []
        for s in self.schedule:
            s[Schedule.course_index].schedule(lesson=s[Schedule.lesson_index], date=self.date, ins=s[Schedule.ins_index])
            s[Schedule.course_index].clear_schedule_buffer()
            if s[Schedule.ins_index] is not None:
                calendar_dict[self.date].append(s[Schedule.ins_index].name)
                apply_adjustment_to_ins(course=s[Schedule.course_index], ins=s[Schedule.ins_index])
        self.schedule = []

    def clean_up(self, calendar_dict):
        calendar_dict[self.date] = []
        for s in self.schedule:
            lesson = s[Schedule.lesson_index]
            lesson.temp_date = None
            lesson.schedule_buffer = False

    def __str__(self):
        return 'Schedule at {}: Lesson is {} '.format(self.date, self.schedule)

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
                    if t[Schedule.course_index] == cur_course:
                        self.point -= t[Schedule.point_index]

                        self.schedule.remove(t)
                self.schedule.append(s)
                self.point += s[Schedule.point_index]

    def update_possible_lessons(self, possible_lessons, course):
        for s in self.schedule:
            if course == s[Schedule.course_index] and s[Schedule.lesson_index] in possible_lessons:
                possible_lessons.remove(s[Schedule.lesson_index])

