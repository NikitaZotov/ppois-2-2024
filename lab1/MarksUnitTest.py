import unittest
from Marks import Marks

class TestMarks(unittest.TestCase):

    def test_add_grade(self):
        marks = Marks()
        marks.add_grade(85)
        self.assertEqual(marks.get_grades(), [85])

    def test_get_grades(self):
        marks = Marks()
        grades = [85, 90, 95]
        for grade in grades:
            marks.add_grade(grade)
        self.assertEqual(marks.get_grades(), grades)

if __name__ == '__main__':
    unittest.main()
