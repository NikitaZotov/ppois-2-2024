import random

from lib.cell import Cell


class CellGenerator:
    @staticmethod
    def generate_cells():
        cells = list()
        cells.append(CellGenerator.generate_safe_cells())

        for _ in range(2):
            cells.append(CellGenerator.generate_random_cell())

        random.shuffle(cells)
        return cells

    @staticmethod
    def generate_safe_cells():
        safe_cell = Cell(
            humidity=random.randint(0, 50),
            electrification=random.randint(0, 50),
            temperature=random.randint(0, 50)
        )
        return safe_cell

    @staticmethod
    def generate_random_cell():
        cell = Cell(
            humidity=random.randint(0, 100),
            electrification=random.randint(0, 100),
            temperature=random.randint(0, 100)
        )
        return cell
