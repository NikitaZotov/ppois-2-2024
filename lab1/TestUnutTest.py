import unittest
from Test import Test

class TestTest(unittest.TestCase):

    def setUp(self):
        self.test = Test("Math Test", ["Q1?", "Q2?"], ["A1", "A2"])

    def test_get_name(self):
        self.assertEqual(self.test.get_name(), "Math Test")

    def test_get_questions(self):
        self.assertEqual(self.test.get_questions(), ["Q1?", "Q2?"])

    def test_get_answers(self):
        self.assertEqual(self.test.get_answers(), ["A1", "A2"])

if __name__ == '__main__':
    unittest.main()
