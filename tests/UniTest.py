import unittest
from files.University import University
from files.Student import Student
from files.Professor import Professor
from files.Curriculum import Curriculum
from files.Classroom import Classroom


class TestUniversity(unittest.TestCase):
    def setUp(self):
        self.university = University("Test University", "Test Address")
        self.student = Student("John", "Doe", 20)
        self.professor = Professor("Jane", "Smith", 35)
        self.curriculum = Curriculum(
            "Test Curriculum", ["Subject1", "Subject2"], {}, 10
        )
        self.classroom = Classroom("101")

    def test_add_student(self):
        self.university.add_student(self.student)
        self.assertIn(self.student, self.university.students)

    def test_remove_student(self):
        self.university.add_student(self.student)
        self.university.remove_student(self.student)
        self.assertNotIn(self.student, self.university.students)

    def test_add_professor(self):
        self.university.add_professor(self.professor)
        self.assertIn(self.professor, self.university.professors)

    def test_add_curriculum(self):
        self.university.add_curriculum(self.curriculum)
        self.assertIn(self.curriculum, self.university.curriculums)

    def test_add_classroom(self):
        self.university.add_classroom(self.classroom)
        self.assertIn(self.classroom, self.university.classrooms)

    def test_find_student(self):
        self.university.add_student(self.student)
        found_student = self.university.find_student("John", "Doe")
        self.assertEqual(found_student, self.student)

    def test_find_professor(self):
        self.university.add_professor(self.professor)
        found_professor = self.university.find_professor("Jane", "Smith")
        self.assertEqual(found_professor, self.professor)


if __name__ == "__main__":
    unittest.main()
