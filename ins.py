import datetime


class Ins:

    pos_adj = 0.4
    neg_adj = -1

    def __init__(self, name):
        self.name = name
        self.pos_adjust_weekdys = []
        self.pos_adjustment = 0
        self.neg_adjust_weekdys = []
        self.neg_adjustment = 0
        self.cur_adjustment = 0.0
        self.cur_adjustment_scale = 1
        self.absent_start = []
        self.absent_end = []
        self.yesterday = -8
        self.max_per_week = 3

    def set_adjustment(self, weekdys, adjust):
        adjust = int(adjust)
        if adjust > 0:
            self.pos_adjust_weekdys = [int(d) for d in weekdys]
            self.pos_adjustment = adjust
        else:
            self.neg_adjust_weekdys = [int(d) for d in weekdys]
            self.neg_adjustment = adjust

    def has_adjustment(self):
        return self.neg_adjustment != 0 or self.pos_adjustment != 0

    def get_adjustment(self, date, calendar_dict):
        for idx,_ in enumerate(self.absent_start):
            if self.absent_start[idx] <= date <= self.absent_end[idx]:
                return -20
        adj = 0
        if date.isoweekday() in self.pos_adjust_weekdys:
            adj = self.pos_adjustment
        if date.isoweekday() in self.neg_adjust_weekdys:
            adj = self.neg_adjustment
        if date - datetime.timedelta(days=1) in calendar_dict and self.name in calendar_dict[date - datetime.timedelta(days=1)]:
            adj += self.yesterday
        return adj

    def update_cur_adjustment(self, adjustment):
        self.cur_adjustment += (self.cur_adjustment_scale * adjustment)

    def set_absent(self, absent_start, absent_end):
        self.absent_start.append(absent_start)
        self.absent_end.append(absent_end)

    def available_this_week(self, calendar_dict, cur):
        if self.max_per_week < 0:
            return False
        count = 0
        for k, v in calendar_dict.items():
            if (cur - k).days <= 7 and self.name in v:
                count += 1
                if count >= self.max_per_week:
                    return False
        return True

    def __repr__(self):
        if self.name is None:
            return 'None'
        return self.name

    def __str__(self):
        if self.name is None:
            return 'None'
        return self.name

    def __eq__(self, other):
        if self is None and other is None:
            return True
        if self is None or other is None:
            return False
        return self.name == other.name
