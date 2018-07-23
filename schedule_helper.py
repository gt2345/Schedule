from lesson import Lesson

# Get a Lesson object by title, if title is not valid, return None
def get_lesson(course, title):
    if title == 'nan':
        return None
    for l in course.lessons[0]:
        if l.title == title:
            return l
    for l in course.lessons[1]:
        if l.title == title:
            return l
    return None


# Check if a lesson has Prerequisite.
# Return true if a lesson does not have prerequisite, or prerequisite lesson has been scheduled
def check_pre(lesson, course):
    pre = get_lesson(title=lesson.lessonDf['Prerequisite'].item(), course=course)
    if pre == None or pre.scheduled == True:
        return True
    return False


def parse_input(classDf):
    lessons = []
    for title in classDf['Title']:
        l = Lesson(title=title, lessonDf=classDf[classDf['Title'].isin([title])])
        lessons.append(l)
    return lessons

