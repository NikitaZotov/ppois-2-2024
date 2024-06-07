import unittest
from lib.cell import Cell
from lib.cell_generator import CellGenerator


class TestCellGenerator(unittest.TestCase):

    def test_generate_cells(self):
        cells = CellGenerator.generate_cells()
        self.assertEqual(len(cells), 3)  # Проверяем, что сгенерированы три ячейки
        for cell in cells:
            self.assertIsInstance(cell, Cell)  # Проверяем, что каждый элемент списка - объект Cell

    def test_generate_safe_cells(self):
        safe_cell = CellGenerator.generate_safe_cells()
        self.assertIsInstance(safe_cell, Cell)  # Проверяем, что сгенерирован безопасный объект Cell
        self.assertLessEqual(safe_cell.humidity, 50)  # Проверяем, что влажность не превышает 50
        self.assertLessEqual(safe_cell.electrification, 50)  # Проверяем, что электрификация не превышает 50
        self.assertLessEqual(safe_cell.temperature, 50)  # Проверяем, что температура не превышает 50

    def test_generate_random_cell(self):
        random_cell = CellGenerator.generate_random_cell()
        self.assertIsInstance(random_cell, Cell)  # Проверяем, что сгенерирован случайный объект Cell
        self.assertLessEqual(random_cell.humidity, 100)  # Проверяем, что влажность не превышает 100
        self.assertLessEqual(random_cell.electrification, 100)  # Проверяем, что электрификация не превышает 100
        self.assertLessEqual(random_cell.temperature, 100)  # Проверяем, что температура не превышает 100


if __name__ == '__main__':
    unittest.main()
