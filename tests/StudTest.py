import unittest
from files.Student import Student
from files.Curriculum import Curriculum
from files.Exam import Exam


class TestStudent(unittest.TestCase):
    def setUp(self):
        self.student = Student("John", "Doe", 20)
        self.curriculum = Curriculum(
            "Computer Science",
            ["Math", "Programming", "Data Structures"],
            {},
            lectures_per_subject=10,
        )

    def test_has_attended_all_lectures(self):
        self.student.curriculum = self.curriculum
        self.student.subjects_attendance = {
            "Math": 10,
            "Programming": 10,
            "Data Structures": 8,
        }
        self.assertTrue(self.student.has_attended_all_lectures())

    def test_attend_lectures(self):
        self.student.curriculum = self.curriculum
        self.student.attend_lectures("Math", 5)
        self.assertEqual(self.student.subjects_attendance["Math"], 5)

    def test_enroll_to_curriculum(self):
        self.student.enroll_to_curriculum(self.curriculum)
        self.assertEqual(self.student.curriculum, self.curriculum)
        self.assertListEqual(
            self.student.courses, ["Math", "Programming", "Data Structures"]
        )

    def test_has_completed_curriculum(self):
        self.student.curriculum = self.curriculum
        self.student.exams = {
            "Math": Exam("Math", "John Doe", "101"),
            "Programming": Exam("Programming", "John Doe", "102"),
            "Data Structures": Exam("Data Structures", "John Doe", "103"),
        }
        for exam in self.student.exams.values():
            exam.passed = True
        self.assertTrue(self.student.has_completed_curriculum())

    def test_reset_curriculum(self):
        self.student.curriculum = self.curriculum
        self.student.courses = ["Math", "Programming", "Data Structures"]
        self.student.subjects_attendance = {
            "Math": 10,
            "Programming": 10,
            "Data Structures": 8,
        }
        self.student.exams = {
            "Math": Exam("Math", "John Doe", "101"),
            "Programming": Exam("Programming", "John Doe", "102"),
            "Data Structures": Exam("Data Structures", "John Doe", "103"),
        }
        self.student.reset_curriculum()
        self.assertIsNone(self.student.curriculum)
        self.assertEqual(self.student.courses, [])
        self.assertEqual(self.student.subjects_attendance, {})
        self.assertEqual(self.student.exams, {})


if __name__ == "__main__":
    unittest.main()
