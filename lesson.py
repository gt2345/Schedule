class Lesson:
    def __init__(self, title, lessonDf):
        self.title = title
        self.lessonDf = lessonDf

        # print(self.lessonDf['Prerequisite'].item())
        self.scheduled = False

    def __str__(self):
        if self.scheduled:
            return "%s scheduled at %s for %s" % (self.title, self.date, self.ins)
        else:
            return "%s not scheduled yet" % (self.title)


    def schedule(self, date, calendar_dict):
        self.scheduled = True
        self.date = date
        ins = self.getIns()
        if self.date in calendar_dict:
            unavailableIns = []
            while ins in calendar_dict[self.date]:
                unavailableIns.append(ins)
                ins = self.getIns(unavailableIns=unavailableIns)
            calendar_dict[self.date].append(ins)
        else:
            calendar_dict[self.date] = [ins]
        self.ins = ins

    def getIns(self, unavailableIns=[]):
        drop_list = ['Title', 'Prerequisite'] + unavailableIns
        return self.lessonDf.drop(drop_list, axis=1).idxmax(axis=1).item()

