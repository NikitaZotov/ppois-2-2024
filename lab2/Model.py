import xml.sax
from SAXparser import StudentHandler
from DOMparser import add_note
from DOMparser import delete_note_by_group
from DOMparser import delete_note
import os

from Student import Student


def is_file_empty(file_path):
    return os.path.getsize(file_path) == 0


class Model:
    def __init__(self, file: str):
        self.students: list = [Student]
        self.amount_of_students: int = 0
        self.file_path = file

    def initialize(self):
        if is_file_empty(self.file_path):
            print("File is empty")
        else:
            parser = xml.sax.make_parser()
            handler = StudentHandler()
            parser.setContentHandler(handler)
            parser.parse(self.file_path)
            self.students.clear()
            for stud in handler.students:
                name: str = stud['name']
                group: str = stud['group']
                exam_titles: list = []
                exam_grades: list = []
                for i in range(len(stud['exam_title'])):
                    exam_titles.append(stud['exam_title'][i])
                    exam_grades.append(int(stud['exam_grade'][i]))
                new_student = Student(name, group, exam_titles, exam_grades)
                self.students.append(new_student)
                self.amount_of_students += 1
        self.print_student()

    def get_student_as_a_list(self, stud_list=None) -> list:
        if stud_list is None:
            stud_list = self.students
        converted_data = []
        for stud in stud_list:
            name = stud.get_name()
            group = stud.get_group()
            exams = []

            for i in range(len(stud.get_exams())):
                exam_titles, exam_grades = zip(*stud.get_exams())
                exam = [exam_titles[i], str(exam_grades[i])]
                exams.append(exam)
            converted_student = [name, group, exams]
            converted_data.append(converted_student)

        return converted_data

    def sort_student_by_group(self):
        self.students.sort(key=lambda stud: stud.get_group())

    def print_student(self):
        print("Students: \n")
        for stud in self.students:
            print(stud)
        print("\n")

    def add_student(self, student: Student):
        print("Student added")
        add_note(self.file_path, student)
        self.initialize()

    def delete_student_by_group(self, group: int) -> int:
        amount: int = 0
        amount = delete_note_by_group(self.file_path, group)
        self.initialize()
        print(amount, "students deleted")
        return amount

    def delete_student_by_av_mark(self, av_mark: float) -> int:
        amount: int = 0
        for stud in self.students:
            if stud.get_avg_grade() == av_mark:
                amount = amount + 1
                delete_note(self.file_path, stud.get_name(), stud.get_group())
        self.initialize()
        print(amount, "students deleted")
        return amount

    def delete_student_by_mark_range(self, min_mark: int, max_mark: int, exam_title: str) -> int:
        amount: int = 0
        for stud in self.students:
            for exam in stud.get_exams():
                title, mark = exam
                if title == exam_title and max_mark >= mark >= min_mark:
                    delete_note(self.file_path, stud.get_name(), stud.get_group())
                    amount = amount + 1
        self.initialize()
        print(amount, "students deleted")
        return amount

    def find_student_by_group(self, student_group: int) -> list:
        new_data: list = []
        for stud in self.students:
            if int(stud.get_group()) == student_group:
                new_data.append(stud)
        print(len(new_data), " found by group")
        return self.get_student_as_a_list(new_data)

    def find_student_by_av_mark(self, av_mark: float) -> list:
        new_data: list = []
        for stud in self.students:
            if stud.get_avg_grade() == av_mark:
                new_data.append(stud)
        print(len(new_data), " found by av mark")
        return self.get_student_as_a_list(new_data)

    def find_student_by_mark_range(self, min_mark: int, max_mark: int, exam_title: str) -> list:
        new_data: list = []
        for stud in self.students:
            for exam in stud.get_exams():
                title, mark = exam
                if title == exam_title and max_mark >= mark >= min_mark:
                    new_data.append(stud)
        print(len(new_data), " found by mark range")
        return self.get_student_as_a_list(new_data)


if __name__ == "__main__":
    model = Model("data.xml")
    model.initialize()
    print(model.find_student_by_mark_range(7, 9, "computer science"))
    model.print_student()
