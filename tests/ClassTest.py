import unittest
from files.Classroom import Classroom


class TestClassroom(unittest.TestCase):
    def setUp(self):
        self.classroom = Classroom("101")

    def test_str(self):
        self.assertEqual(str(self.classroom), "101")


if __name__ == "__main__":
    unittest.main()
