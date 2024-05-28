import unittest
from unittest.mock import patch
from Teacher import Teacher
from Student import Student
from Test import Test

class TestTeacher(unittest.TestCase):

    def setUp(self):
        self.teacher = Teacher()
        self.student = Student("John Doe")
        self.test = Test("Math Test", ["Q1?", "Q2?"], ["A1", "A2"])

    @patch('builtins.input', side_effect=['A1', 'A2'])
    def test_test_student(self, mock_input):
        self.teacher.test_student(self.student, self.test)
        self.assertEqual(self.student.get_marks("Math Test").get_grades(), [10])

    def test_add_test(self):
        tests = []
        self.teacher.add_test(tests, self.test)
        self.assertEqual(len(tests), 1)
        self.assertEqual(tests[0].get_name(), "Math Test")

    def test_remove_test(self):
        tests = [self.test]
        self.teacher.remove_test(tests, "Math Test")
        self.assertEqual(len(tests), 0)

if __name__ == '__main__':
    unittest.main()
