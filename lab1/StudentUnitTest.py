import unittest
from unittest.mock import patch
from Student import Student
from Marks import Marks
from Feedback import Feedback
from Test import Test

class TestStudent(unittest.TestCase):

    def setUp(self):
        self.student = Student("John Doe")

    def test_get_name(self):
        self.assertEqual(self.student.get_name(), "John Doe")

    def test_add_feedback(self):
        feedback = Feedback("Well done!")
        self.student.add_feedback(feedback)
        self.assertEqual(len(self.student.get_feedbacks()), 1)
        self.assertEqual(self.student.get_feedbacks()[0].get_message(), "Well done!")

    @patch('builtins.input', side_effect=['This is a feedback message.'])
    def test_create_feedback(self, mock_input):
        self.student.create_feedback()
        self.assertEqual(len(self.student.get_feedbacks()), 1)
        self.assertEqual(self.student.get_feedbacks()[0].get_message(), "This is a feedback message.")

    def test_add_grade(self):
        self.student.add_grade("Math", 90)
        self.assertIsInstance(self.student.get_marks("Math"), Marks)
        self.assertEqual(self.student.get_marks("Math").get_grades(), [90])

if __name__ == '__main__':
    unittest.main()
