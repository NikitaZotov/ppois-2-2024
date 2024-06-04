class Marks:
    def __init__(self):
        self.grades = []

    def add_grade(self, grade) -> None:
        self.grades.append(grade)

    def get_grades(self) -> list:
        return self.grades

