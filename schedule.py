import copy


class Schedule:
    def __init__(self, courses):
        self.courses = []
        for c in courses:
            self.courses.append(copy.deepcopy(c))