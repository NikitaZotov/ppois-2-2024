import re

from files.Person import Person
from files.Library import Library
from typing import List, Optional, Dict
from files.Curriculum import Curriculum
from files.Exam import Exam
from files.Scholarship import Scholarship


class Student(Person):
    def __init__(self, first_name: str, last_name: str, age: int) -> None:
        super().__init__(first_name, last_name, age)
        self.courses: List[str] = []
        self.curriculum: Optional[Curriculum] = None
        self.subjects_attendance: Dict[str, int] = {}
        self.library_books: List[str] = []
        self.exams: Dict[str, Exam] = {}
        self.balance = 0
        self.attended_lectures = False

    def has_attended_all_lectures(self) -> bool:
        if not self.curriculum:
            return False
        for subject in self.curriculum.subjects:
            if subject not in self.subjects_attendance:
                return False
        return True

    def attend_lectures(self, subject: str, lectures_attended: int) -> None:
        if self.has_attended_all_lectures():
            print(
                "Вы уже посетили все учебные занятия. Повторное посещение невозможно."
            )
            return
        if self.curriculum and subject in self.curriculum.subjects:
            self.subjects_attendance[subject] = lectures_attended
        else:
            print(
                "Вы еще не выбрали учебный план или предмет не найден в выбранном учебном плане."
            )

    @classmethod
    def validate_name(cls, name: str) -> bool:
        if not re.match("^[А-ЯЁ][а-яё]*$", name) and not re.match(
            "^[A-Z][a-z]*$", name
        ):
            return False
        return True

    @staticmethod
    def validate_age(age: int) -> bool:
        if 16 <= age <= 100:
            return True
        return False

    def enroll_to_curriculum(self, curriculum: Curriculum) -> None:
        self.curriculum = curriculum
        self.courses.extend(curriculum.subjects)

    def borrow_book(self, library):
        print("Список доступных книг в библиотеке:")
        available_books = library.display_available_books()

        book_to_borrow = input("Выберите книгу: ")
        if book_to_borrow in available_books:
            if book_to_borrow not in self.library_books:
                if library.lend_book(book_to_borrow, self.first_name, self.last_name):
                    self.library_books.append(book_to_borrow)
            else:
                print("У вас уже есть эта книга.")

    def return_book(self, library: Library) -> None:
        print("Список ваших книг:")
        for book in self.library_books:
            print(book)

        book_to_return = input("Выберите книгу для сдачи: ")
        if book_to_return in self.library_books:
            library.return_book(book_to_return, self.first_name, self.last_name)
            self.library_books.remove(book_to_return)
        else:
            print("У вас нет этой книги.")

    def display_student_books(self) -> None:
        if self.library_books:
            for book in self.library_books:
                print(book)
        else:
            print("У вас нет книг.")

    def receive_stipend(self):
        if self.curriculum is not None and len(self.exams) == len(
            self.curriculum.subjects
        ):
            if not self.exams:
                print("Студент еще не сдал ни одного экзамена.")
                return

            total_grade = sum(exam.grade for exam in self.exams.values())
            average_grade = total_grade / len(self.exams)

            stipend = Scholarship.calculate_stipend(average_grade)

            if stipend >= 0:
                self.balance += stipend
                print(f"Студент получил стипендию в размере {stipend}р.")
            else:
                print("Студент не получил стипендию из-за низкой успеваемости.")

    def has_completed_curriculum(self) -> bool:
        if self.curriculum is None:
            return True
        for subject in self.curriculum.subjects:
            if subject not in self.exams or not self.exams[subject].passed:
                return False
        return True

    def reset_curriculum(self):
        self.curriculum = None
        self.courses.clear()
        self.subjects_attendance.clear()
        self.exams.clear()
