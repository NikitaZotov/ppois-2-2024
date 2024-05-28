import unittest
from files.Professor import Professor


class TestProfessor(unittest.TestCase):
    def test_constructor(self):
        professor = Professor("John", "Doe", 40)
        self.assertEqual(professor.first_name, "John")
        self.assertEqual(professor.last_name, "Doe")
        self.assertEqual(professor.age, 40)


if __name__ == "__main__":
    unittest.main()
