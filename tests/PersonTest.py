import unittest
from files.Person import Person


class TestPerson(unittest.TestCase):
    def test_constructor(self):
        person = Person("John", "Doe", 30)
        self.assertEqual(person.first_name, "John")
        self.assertEqual(person.last_name, "Doe")
        self.assertEqual(person.age, 30)


if __name__ == "__main__":
    unittest.main()
