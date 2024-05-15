from unittest import TestCase

import colors
from management import Management


class TestManagement(TestCase):
    def setUp(self):
        self.management: Management = Management()

    def test_income(self):
        self.management.income(1500)
        self.assertEqual(self.management.account, 1500)

    def test_expense(self):
        self.management.income(1500)
        self.management.expense(1000)
        self.assertEqual(self.management.account, 500)

    def test_show_history(self):
        self.management.income(10)
        self.management.expense(5)
        hist: str = (f'{colors.CGREEN}income{colors.CEND}: 10\n'
                     f'{colors.CRED}expense{colors.CEND}: 5\n')
        self.assertEqual(self.management.show_history(), hist)
