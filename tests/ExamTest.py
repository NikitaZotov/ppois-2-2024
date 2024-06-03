import unittest
from files.Exam import Exam


class TestExam(unittest.TestCase):
    def setUp(self):
        self.exam = Exam("Math", "John Doe", "101")

    def test_take_exam_passed(self):
        # Успешное сдача экзамена (оценка >= 4)
        self.exam.take_exam(10, 10)  # 100% посещаемость
        self.assertTrue(self.exam.passed)
        self.assertGreaterEqual(self.exam.grade, 4)


if __name__ == "__main__":
    unittest.main()
