class Ins:

    pos_adj = 0.2
    neg_adj = -0.5

    def __init__(self, name):
        self.name = name
        self.pos_adjust_weekdys = []
        self.pos_adjustment = 0
        self.neg_adjust_weekdys = []
        self.neg_adjustment = 0
        self.cur_adjustment = 0.0
        self.cur_adjustment_scale = 1
        self.absent_start = 0
        self.absent_end = 0

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

    def get_adjustment(self, date):
        if self.absent_start != 0 and self.absent_start <= date <= self.absent_end:
            return -20
        if date.isoweekday() in self.pos_adjust_weekdys:
            return self.pos_adjustment
        if date.isoweekday() in self.neg_adjust_weekdys:
            return self.neg_adjustment
        return 0

    def update_cur_adjustment(self, adjustment):
        self.cur_adjustment += (self.cur_adjustment_scale * adjustment)

    def set_absent(self, absent_start, absent_end):
        self.absent_start = absent_start
        self.absent_end = absent_end

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name
