import datetime
import pandas as pd


class Lesson:

    def __init__(self, id, title, lesson_df, code, week):
        self.title = title
        self.id = id
        self.lesson_df = lesson_df
        self.code = code
        self.week = week
        self.number = -1
        self.practice = ('Practice' in self.title)
        # print(self.lessonDf['Prerequisite'].item())
        self.scheduled = False
        self.schedule_buffer = False
        self.temp_date = None
        self.date = None
        self.ins = None
        self.pre_scheduled = False

    def __str__(self):
        if self.scheduled:
            return "%s %d %s scheduled at %s for %s" % (self.code, self.number, self.title, self.date, self.ins)
        else:
            return "%s %s not scheduled yet" % (self.code, self.title)

    def __repr__(self):
        return self.title

    def schedule(self, date, ins, number):
        self.scheduled = True
        self.date = date
        self.number = number
        self.ins = ins

    def is_scheduled(self):
        return self.scheduled or self.schedule_buffer

    def get_date(self):
        if self.date is not None:
            return self.date
        else:
            return self.temp_date


