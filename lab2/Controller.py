from Model import Model
from Student import Student
from View import MainWindow, show_warning
from PyQt5.QtWidgets import QApplication, QFileDialog
import sys
import shutil


class Controller:
    def __init__(self):
        app = QApplication(sys.argv)
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(None, "Open File", "", "*.xml")
        self.file_path = file_path
        self.model: Model = Model(self.file_path)
        self.model.initialize()
        self.data = self.model.get_student_as_a_list
        self.view = MainWindow(self.data())
        self.view.add_signal.connect(self.add_student)
        self.view.del_signal.connect(self.delete_student_switcher)
        self.view.find_signal.connect(self.find_student_switcher)
        self.view.save_file_signal.connect(self.save_file)
        self.view.open_signal.connect(self.open_file)
        self.view.show()
        sys.exit(app.exec_())

    def open_file(self, new_file_path):
        print(new_file_path)
        self.file_path = new_file_path
        self.model: Model = Model(self.file_path)
        self.model.initialize()
        self.data = self.model.get_student_as_a_list
        self.view.table.reload_table(self.data())

    def save_file(self, new_file: str) -> None:
        if self.file_path:
            shutil.copy(self.file_path, new_file)

    def add_student(self, student: list):
        name = student[0]
        group = student[1]
        exams = student[2]
        exam_titles, exam_grades = zip(*exams)
        print(exam_titles)
        print(exam_grades)
        converted_grades = []
        for grade in exam_grades:
            converted_grades.append(int(grade))

        new_student = Student(name, group, exam_titles, converted_grades)
        self.model.add_student(new_student)
        self.view.table.reload_table(self.data())

    def delete_student_switcher(self, del_type_and_data):
        print("del switch")
        del_type, data = del_type_and_data
        amount_of_deletions: int = 0
        if del_type == "by_group":
            amount_of_deletions = self.model.delete_student_by_group(data[0])
        elif del_type == "by_av_mark":
            amount_of_deletions = self.model.delete_student_by_av_mark(data[0])
        elif del_type == "by_mark_range":
            amount_of_deletions = self.model.delete_student_by_mark_range(int(data[0]), int(data[1]), data[2])
        msg: str = str(amount_of_deletions) + " students were deleted"
        show_warning(msg)
        self.view.table.reload_table(self.data())

    def find_student_switcher(self, find_type_and_data):
        print("find switch")
        new_data: list = self.data()
        find_type, data = find_type_and_data

        if find_type == "by_group":
            new_data = self.model.find_student_by_group(data[0])
        elif find_type == "by_av_mark":
            new_data = self.model.find_student_by_av_mark(data[0])
        elif find_type == "by_mark_range":
            new_data = self.model.find_student_by_mark_range(int(data[0]), int(data[1]), data[2])
        msg: str = str(len(new_data)) + " students were found"
        show_warning(msg)
        print(new_data)
        self.view.retrieve_signal.emit(new_data)


if __name__ == '__main__':
    controller = Controller()
