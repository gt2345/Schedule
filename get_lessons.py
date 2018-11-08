def get_possible_lessons_detail(course, cur_date, consider_week):
    possible_lessons = []
    for l in course.lessons:
        if not l.is_scheduled():

            # Practice Class 01 corner case
            if l.code[0] == 1:
                if l.code[1] == 1 and not get_lesson(course=course, code=[1, 1]).is_scheduled():
                    possible_lessons.append(l)
                    break
                elif get_lesson(course=course, code=[1, 1]).is_scheduled():
                    possible_lessons.append(l)
            elif l.pre_req > 0:
                if get_lesson(course=course,id=l.pre_req).is_scheduled():
                    possible_lessons.append(l)
            elif (l.week == 0 or (l.week > 0 and l.code[1] == 1)) and \
                    ((l.week > 0 and l.code[1] == 1 and get_lesson(course=course, code=[l.code[0] - 2, 1]).is_scheduled()) or \
                    (l.code[1] > 1 and get_lesson(course=course, code=[l.code[0], l.code[1] - 1]).is_scheduled()) or \
                    (l.code[1] <= 1 and get_lesson(course=course, code=[l.code[0] - 1, 1]).is_scheduled())):
                possible_lessons.append(l)
            elif l.week > 0:
                if l.code[1] > 1:
                    pre_lesson = get_lesson(course=course, code=[l.code[0], l.code[1] - 1])
                else:
                    pre_lesson = get_lesson(course=course, code=[l.code[0] - 1, 1])

                if pre_lesson.is_scheduled():
                    if consider_week is False or (cur_date - pre_lesson.get_date()).days >= l.week:
                        possible_lessons.append(l)
    return possible_lessons


# first time separate week attribute lessons be week_separator
# if no available lessons, disregard week_separator
def get_possible_lessons(course, cur_date):
    possible_lessons = get_possible_lessons_detail(course=course, cur_date=cur_date, consider_week=True)
    if len(possible_lessons) == 0: # or (len(possible_lessons) == 1 and possible_lessons[0].week == 0):
        possible_lessons = get_possible_lessons_detail(course=course, cur_date=cur_date, consider_week=False)
    return possible_lessons

# Get a Lesson object by title, if title is not valid, return None
def get_lesson(course, title=None, code=None, id=None):
    if title is None and code is None and id is None:
        return None

    if id is not None:
        for l in course.lessons:
            if l.id == id:
                return l

    if title is not None:
        for l in course.lessons:
            if l.title == title:
                return l

    if code is not None:
        for l in course.lessons:
            if l.code == code:
                return l

    return None