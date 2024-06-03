import unittest
from files.Library import Library


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.library = Library()

    def test_add_book(self):
        self.library.add_book("Book 1", 5)
        self.library.add_book("Book 2", 3)
        self.assertEqual(self.library.books["Book 1"], 5)
        self.assertEqual(self.library.books["Book 2"], 3)

    def test_display_available_books(self):
        self.library.add_book("Book 1", 5)
        self.library.add_book("Book 2", 3)
        available_books = self.library.display_available_books()
        self.assertIn("Book 1", available_books)
        self.assertIn("Book 2", available_books)

    def test_lend_book(self):
        self.library.add_book("Book 1", 5)
        self.library.lend_book("Book 1", "John", "Doe")
        self.assertEqual(self.library.books["Book 1"], 4)
        self.assertIn(("John", "Doe"), self.library.borrowers)
        self.assertIn("Book 1", self.library.borrowers[("John", "Doe")])

    def test_return_book(self):
        self.library.add_book("Book 1", 5)
        self.library.lend_book("Book 1", "John", "Doe")
        self.library.return_book("Book 1", "John", "Doe")
        self.assertEqual(self.library.books["Book 1"], 5)
        self.assertNotIn("Book 1", self.library.borrowers[("John", "Doe")])


if __name__ == "__main__":
    unittest.main()
