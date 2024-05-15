from unittest import TestCase

from furniture import Table
from people import Visitor


class TestFurniture(TestCase):
    def setUp(self):
        self.table: Table = Table()
        self.visitor: Visitor = Visitor()

    def test_take_table(self):
        self.table.take_table(self.visitor)
        self.assertEqual(self.table.is_taken, True)

    def test_checked_chairs(self):
        self.table.take_table(self.visitor)
        chair_is_taken: bool = False
        for chair in self.table.chairs:
            if chair.is_taken:
                chair_is_taken = True
        self.assertEqual(chair_is_taken, True)

    def test_take_taken_table(self):
        self.table.take_table(self.visitor)
        visitor2: Visitor = Visitor()
        self.table.take_table(visitor2)
        taken_chairs: int = 0
        for chair in self.table.chairs:
            if chair.is_taken:
                taken_chairs += 1
        self.assertEqual(taken_chairs, 1)
        self.assertEqual(self.table.is_taken, True)
        self.assertEqual(self.table.visitor, self.visitor)

    def test_free_table(self):
        self.table.take_table(self.visitor)
        self.assertEqual(self.table.visitor, self.visitor)
        self.table.free_table()
        self.assertEqual(self.table.is_taken, False)
        self.assertNotEqual(self.table.visitor, self.visitor)
