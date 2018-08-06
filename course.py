from day_iter import DayIter


class Course:

    week_separator = 3

    def __init__(self, title, start_date, weekdys, lessons, ins):
        self.title = title
        self.weekdys = weekdys
        self.lessons = lessons # array of lessons
        self.ins = ins
        self.start_date = start_date
        self.iter = DayIter(start_date=start_date, weekdys=str(weekdys))
        self.class_list = []
        self.class_scheduled = 1
        self.practice_scheduled = 0
        self.practice_total = self.count_practice()
        self.class_total = len(self.lessons) - self.practice_total

    def count_practice(self):
        count = 0
        for x in self.lessons:
            if 'Practice' in x.title:
                count += 1
        return count

    def schedule(self, lesson, date, ins):
        if lesson.practice:
            self.practice_scheduled += 1
            lesson.schedule(date=date, ins=ins, number=self.practice_scheduled)
        else:
            self.class_scheduled += 1
            lesson.schedule(date=date, ins=ins, number=self.class_scheduled)
        #self.class_list.append([date, self.title, lesson.number, lesson.title, lesson.ins])
        self.class_list.append(lesson)
        self.iter.__next__()

    def reset_iter(self, start_date):
        self.iter = DayIter(start_date=start_date, weekdys=str(self.weekdys))

    def clear_schedule_buffer(self):
        for l in self.lessons:
            l.schedule_buffer = False

    def complete(self):
        return self.class_scheduled >= self.class_total - 1 and self.practice_scheduled >= self.practice_total

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title