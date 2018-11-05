from course import Course
from ins import Ins


# return (ins, point)
def get_ins(lesson, course, calendar_dict, date, unavailable_ins):
    drop_list = ['Title', 'Sequence', 'Order', 'Id', 'Week'] + unavailable_ins
    cur_lesson_df = apply_adjustment(course=course, to_be_scheduled_lesson=lesson, date=date, calendar_dict=calendar_dict)
    #print(cur_lesson_df)
    cur_lesson_df = cur_lesson_df.drop(drop_list, axis=1)
    try:
        ins_name = cur_lesson_df.idxmax(axis=1).item()
    except ValueError:
        return None, 0
    ins = get_ins_by_name(course=course, name=ins_name)

    if date not in calendar_dict:
        calendar_dict[date] = []

    # ins is not scheduled for today or yesterday
    while ins is not None and (ins.name in calendar_dict[date] or not ins.available_this_week(calendar_dict=calendar_dict,cur=date)):
        unavailable_ins.append(ins.name)
        if course.no_available_ins(unavailable_ins):
            break
        ins = get_ins(lesson=lesson, course=course, unavailable_ins=unavailable_ins, calendar_dict=calendar_dict, date=date)[0]

    if ins is None:
        return None, 0
    if cur_lesson_df[ins.name].item() > 0:
        return ins, cur_lesson_df[ins.name].item()
    else:
        return None, 0


def get_ins_by_name(course, name):
    for i in course.ins:
        if i.name == name:
            return i
    return None


# if an ins is scheduled for a lesson, all following lesson get Ins.neg_adj and all other ins get Ins.pos_adj
# but positive adjustment do not add up to more than 2
def apply_adjustment_to_ins(course, ins):
    ins.update_cur_adjustment(Ins.neg_adj)
    for cur_ins in course.ins:
        if cur_ins != ins and cur_ins.cur_adjustment <= 0:
            cur_ins.update_cur_adjustment(Ins.pos_adj)


def apply_adjustment(to_be_scheduled_lesson, date, course, calendar_dict):
    cur_lesson_df = to_be_scheduled_lesson.lesson_df[
        to_be_scheduled_lesson.lesson_df['Id'] == to_be_scheduled_lesson.id]
    # apply adjustment from lessons
    counter = 0
    if to_be_scheduled_lesson.id <= Course.prefer_to_be_ordered_up_to:
        for l in course.lessons:
            if l.id >= to_be_scheduled_lesson.id or l.id > Course.prefer_to_be_ordered_up_to:
                continue
            if not l.is_scheduled():
                counter += 1

    # apply adjustment from ins and from not scheduled
    for ins in course.ins:
        adj = ins.get_adjustment(date=date, calendar_dict=calendar_dict) - (counter * Course.not_scheduled_scale)
        if cur_lesson_df.loc[:, ins.name].item() != 0:
            cur_lesson_df.loc[:, ins.name] += (adj + ins.cur_adjustment)
    return cur_lesson_df


