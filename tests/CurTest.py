import unittest
from files.Curriculum import Curriculum
from files.Professor import Professor


class TestCurriculum(unittest.TestCase):
    def setUp(self):
        self.professors = {
            "Math": Professor("John", "Doe", 40),
            "Physics": Professor("Alice", "Smith", 35),
        }
        self.curriculum = Curriculum(
            "Computer Science", ["Math", "Physics"], self.professors
        )


if __name__ == "__main__":
    unittest.main()
