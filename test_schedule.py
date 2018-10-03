from unittest import TestCase

from course import Course
from parse import *
import pandas as pd
class_input = 'Input/Punch card - Final 0806.csv'
ins_adjustment_input = 'Input/Ins.csv'

lesson_df = pd.read_csv(class_input).fillna(0)

# create job ob
ins_list = parse_ins(lesson_df, ins_df=pd.read_csv(ins_adjustment_input).fillna(0))
course2 = Course(title='Summer02', start_date=date(2018, 6, 30), weekdys=13567,
                 lessons=parse_lesson(lesson_df), ins=get_ins_list(ins_list=ins_list, ins_array=['Jin']))
schedule = Schedule(date=date(2018, 7, 30))
# schedule.add_course(course=course2, lesson=get_lesson(course=course2, id=101),)
