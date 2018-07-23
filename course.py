from day_iter import DayIter

class Course:

    def __init__(self, title, start_date, weekdys, lessons):
        self.title = title
        self.lessons = lessons # array of lessons
        self.start_date = start_date
        self.iter = DayIter(start_date=start_date, weekdys=str(weekdys))
        self.class_list = []
        self.class_scheduled = 0
        self.practice_scheduled = 0

