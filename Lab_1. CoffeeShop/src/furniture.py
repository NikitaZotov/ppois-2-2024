import random
from typing import List

import exceptions
from people import Visitor


class Chair:
    def __init__(self):
        self.is_taken: bool = False

    def take_chair(self) -> None:
        self.is_taken = True

    def free_chair(self) -> None:
        self.is_taken = False


class Table:
    def __init__(self):
        self.chairs: List[Chair] = []
        self.visitor = None
        for i in range(1, random.randint(2, 4)):
            self.chairs.append(Chair())

    @property
    def is_taken(self) -> bool:
        for chair in self.chairs:
            if chair.is_taken:
                return True
        return False

    def take_table(self, visitor: Visitor) -> bool:
        try:
            if self.is_taken:
                raise exceptions.TakenException()
            else:
                self.chairs[random.randint(0, len(self.chairs) - 1)].take_chair()
                self.visitor = visitor
                return True
        except exceptions.TakenException:
            return False

    def free_table(self) -> None:
        for chair in self.chairs:
            self.visitor = None
            chair.free_chair()
