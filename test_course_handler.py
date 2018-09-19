from unittest import TestCase
from schedule_helper_basic import *


class TestCourse_handler(TestCase):
    def test_course_handler(self):
        courses = [1, 2, 3]
        res = course_handler(courses)
        self.assertEqual(res, [[1,2,3],[1,3,2]])
