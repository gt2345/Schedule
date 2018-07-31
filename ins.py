class Ins:

    def __init__(self, name):
        self.name = name
        self.pos_adjust_weekdys = []
        self.pos_adjustment = 0
        self.neg_adjust_weekdys = []
        self.neg_adjustment = 0

    def set_adjustment(self, weekdys, adjust):
        if adjust > 0:
            self.pos_adjust_weekdys = [int(d) for d in weekdys]
            self.pos_adjustment = adjust
        else:
            self.neg_adjust_weekdys = [int(d) for d in weekdys]
            self.neg_adjustment = adjust

    def has_adjustment(self):
        return self.neg_adjustment != 0 or self.pos_adjustment != 0

    def get_adjustment(self, date):
        if date.isoweekday() in self.pos_adjust_weekdys:
            return self.pos_adjustment
        if date.isoweekday() in self.neg_adjust_weekdys:
            return self.neg_adjustment
        return 0


    def __repr__(self):
        return self.name