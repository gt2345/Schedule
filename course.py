from day_iter import DayIter


class Course:
    # week_separator = 3
    prefer_to_be_ordered_up_to = 1200
    not_scheduled_scale = 2

    def __init__(self, title, start_date, weekdys, lessons, ins, unavailable_ins):
        self.title = title
        self.weekdys = weekdys
        self.lessons = lessons # array of lessons
        self.ins = self.get_ins_list(ins_list=ins, ins_array=unavailable_ins)
        self.unavailable_ins = unavailable_ins
        self.start_date = start_date
        self.iter = DayIter(start_date=start_date, weekdys=str(weekdys))
        self.class_list = []
        self.class_scheduled = 1
        self.practice_scheduled = 0
        self.practice_total = self.count_practice()
        self.class_total = len(self.lessons) - self.practice_total
        self.is_completed = self.class_scheduled >= self.class_total - 1 and self.practice_scheduled >= self.practice_total

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
        self.is_completed = self.class_scheduled >= self.class_total - 1 \
                            and self.practice_scheduled >= self.practice_total
        return self.is_completed

    def get_last_lesson(self):
        res = []
        for l in self.lessons:
            if not l.is_scheduled():
                res.append(l)
        return res

    def no_available_ins(self, unavailable_ins):
        for i in self.ins:
            if not i.name in unavailable_ins:
                return False
        return True

    def has_lesson(self, date):
        return date >= self.start_date and str(date.isoweekday()) in list(str(self.weekdys))

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    def __eq__(self, other):
        return self.title == other.title

    def __hash__(self):
        return hash(self.title)

    def all_scheduled(self):
        for l in self.lessons:
            if not l.is_scheduled():
                return False
        return True


    def get_ins_list(self, ins_list, ins_array):
        res_ins_list = []
        for ins in ins_list:
            if not ins.name in ins_array:
                res_ins_list.append(ins)
        return res_ins_list

