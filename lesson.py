import datetime

class Lesson:

    def __init__(self, title, lessonDf, code):
        self.title = title
        self.lessonDf = lessonDf
        self.code = [int(d) for d in str(code)]
        if len(self.code) == 3:
            self.code = [self.code[0] * 10 + self.code[1], self.code[2]]
        self.number = -1
        self.practice = ('Practice: ' in self.title)
        # print(self.lessonDf['Prerequisite'].item())
        self.scheduled = False
        self.date = None
        self.ins = None

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

    def get_ins(self, calendar_dict, date, unavailableIns):
        # drop_list = ['Title', 'Prerequisite'] + unavailableIns
        drop_list = ['Title', 'Code'] + unavailableIns
        # lessonDf = classDf[classDf['Title'].isin([title])]

        ins = self.lessonDf[self.lessonDf['Title'].isin([self.title])].drop(drop_list, axis=1).idxmax(axis=1).item()

        if date not in calendar_dict:
            calendar_dict[date] = []

        while (ins in calendar_dict[date]) or \
                 (date - datetime.timedelta(days=1) in calendar_dict and ins in calendar_dict[date - datetime.timedelta(days=1)]):
            if str(ins) != 'nan':
                unavailableIns.append(ins)
            ins = self.get_ins(unavailableIns=unavailableIns, calendar_dict=calendar_dict, date=date)

        # print('At {} for class {} ins is {} '.format(date, self.title, ins))
        return ins

