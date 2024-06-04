import unittest
from Feedback import Feedback

class TestFeedback(unittest.TestCase):

    def test_get_message(self):
        message = "This is a test message."
        feedback = Feedback(message)
        self.assertEqual(feedback.get_message(), message)

if __name__ == '__main__':
    unittest.main()