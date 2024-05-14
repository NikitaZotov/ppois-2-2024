from classes.Timer import Timer
import time
import unittest


class TestTimer(unittest.TestCase):

    def test_constructor(self):
        timer = Timer(60)
        self.assertEqual(timer.duration, 60)
        self.assertEqual(timer.is_running, False)

    def test_duration_setter(self):
        timer = Timer(60)
        timer.duration = 10
        self.assertEqual(timer.duration, 10)

    def test_reset_timer(self):
        timer = Timer(60)
        timer.reset()
        self.assertEqual(timer.duration, 0)
        self.assertEqual(timer.is_running, False)

    def test_start_timer(self):
        timer = Timer(1)
        timer.start()
        self.assertEqual(timer.is_running, True)

    def test_run_timer(self):
        timer = Timer(1)
        timer.start()
        self.assertEqual(timer.is_running, True)
        time.sleep(2)
        self.assertEqual(timer.is_running, False)

if __name__ == '__main__':
    unittest.main()
