import unittest
from files.Scholarship import Scholarship


class TestScholarship(unittest.TestCase):
    def test_calculate_stipend(self):
        # Проверяем, что при средней оценке 10.0 стипендия равна 1000
        self.assertEqual(Scholarship.calculate_stipend(10.0), 1000)

        # Проверяем, что при средней оценке в диапазоне от 7.0 до 10.0 стипендия равна 850
        self.assertEqual(Scholarship.calculate_stipend(9.0), 850)

        # Проверяем, что при средней оценке в диапазоне от 5.0 до 7.0 стипендия равна 750
        self.assertEqual(Scholarship.calculate_stipend(6.5), 750)

        # Проверяем, что при средней оценке в диапазоне от 4.0 до 5.0 стипендия равна 600
        self.assertEqual(Scholarship.calculate_stipend(4.5), 600)

        # Проверяем, что при средней оценке ниже 4.0 стипендия равна 0
        self.assertEqual(Scholarship.calculate_stipend(3.5), 0)


if __name__ == "__main__":
    unittest.main()
