import datetime

class DayIter:
    def __init__(self, start_date, weekdys):
        self.start_date = start_date
        self.weekdys = list(weekdys)
        self.cur = start_date
        while True:
            # print(self.cur.isoweekday())
            if str(self.cur.isoweekday()) in self.weekdys:
                return
            self.cur += datetime.timedelta(days=1)

    def __next__(self):
        res = self.cur
        self.cur += datetime.timedelta(days=1)
        while True:
            if str(self.cur.isoweekday()) in self.weekdys:
                break
            self.cur += datetime.timedelta(days=1)
        return res

    def peek(self):
        return self.cur

    def peek_second(self):
        res = self.cur
        res += datetime.timedelta(days=1)
        while True:
            if str(res.isoweekday()) in self.weekdys:
                break
            res += datetime.timedelta(days=1)
        return res
