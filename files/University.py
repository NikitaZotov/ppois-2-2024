from files.Student import Student
from files.Professor import Professor
from files.Curriculum import Curriculum
from files.Library import Library
from files.Classroom import Classroom
from typing import Optional, List


class University:
    def __init__(self, name: str, address: str) -> None:
        self.name: str = name
        self.address: str = address
        self.students: list[Student] = []
        self.professors: list[Professor] = []
        self.curriculums: list[Curriculum] = []
        self.classrooms: List[Classroom] = []
        self.library: Library = Library()

    def add_student(self, student: Student) -> None:
        if self.find_student(student.first_name, student.last_name) is None:
            self.students.append(student)
            print(f"Студент {student.first_name} {student.last_name} добавлен.")
        else:
            print(f"Студент {student.first_name} {student.last_name} уже существует.")

    def remove_student(self, student: Student) -> None:
        if student in self.students:
            self.students.remove(student)
            print(f"Студент {student.first_name} {student.last_name} исключён.")
        else:
            print(f"Студент {student.first_name} {student.last_name} не найден.")

    def add_professor(self, professor: Professor) -> None:
        if self.find_professor(professor.first_name, professor.last_name) is None:
            self.professors.append(professor)
            print(
                f"Преподаватель {professor.first_name} {professor.last_name} добавлен."
            )
        else:
            print(
                f"Преподаватель {professor.first_name} {professor.last_name} уже существует."
            )

    def add_curriculum(self, curriculum: Curriculum) -> None:
        self.curriculums.append(curriculum)

    def add_classroom(self, classroom: Classroom) -> None:
        self.classrooms.append(classroom)

    def find_student(self, first_name: str, last_name: str) -> Optional[Student]:
        for student in self.students:
            if student.first_name == first_name and student.last_name == last_name:
                return student
        return None

    def find_professor(self, first_name: str, last_name: str) -> Optional[Professor]:
        for professor in self.professors:
            if professor.first_name == first_name and professor.last_name == last_name:
                return professor
        return None
