import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QLabel, \
    QLineEdit, QPushButton, QWidget, QAction, QMessageBox, QComboBox, QHBoxLayout, QSpinBox, QFileDialog


def show_warning(msg: str):
    print("MSG box")
    message_box = QMessageBox()
    message_box.setIcon(QMessageBox.Warning)
    message_box.setWindowTitle("Warning")
    message_box.setText(msg)
    message_box.setStandardButtons(QMessageBox.Ok)
    message_box.exec_()


def contains_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


class StudentTable(QWidget):

    def __init__(self, _data: list):
        self.unique_exams: set = set()
        self.storing_data = _data
        self.current_page = 0
        self.items_per_page = 10

        super().__init__()

        self.table = QTableWidget()
        self.table.setRowCount(self.items_per_page)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ФИО", "Группа", "Экзамены"])

        self.layout_widgets()

        self.populate_table()

    def layout_widgets(self):
        self.layout = QVBoxLayout()

        self.layout.addWidget(self.table)

        button_layout = QHBoxLayout()
        self.begin_button = QPushButton("<<")
        self.begin_button.clicked.connect(self.show_begin_page)
        self.previous_button = QPushButton("<")
        self.previous_button.clicked.connect(self.show_previous_page)
        self.next_button = QPushButton(">")
        self.next_button.clicked.connect(self.show_next_page)
        self.end_button = QPushButton(">>")
        self.end_button.clicked.connect(self.show_end_page)
        button_layout.addWidget(self.begin_button)
        button_layout.addWidget(self.previous_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.end_button)

        # Add a spin box to choose the number of items per page
        self.items_per_page_spinbox = QSpinBox()
        self.items_per_page_spinbox.setMinimum(1)
        self.items_per_page_spinbox.setValue(self.items_per_page)
        self.items_per_page_spinbox.valueChanged.connect(self.change_items_per_page)
        button_layout.addWidget(QLabel("Items per page:"))
        button_layout.addWidget(self.items_per_page_spinbox)

        # Add a label to show the current page
        self.current_page_label = QLabel(f"Page: {self.current_page + 1}")
        button_layout.addWidget(self.current_page_label)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

    def change_items_per_page(self, value):
        self.items_per_page = value
        self.table.setRowCount(self.items_per_page)
        self.populate_table()

    def update_page_label(self):
        self.current_page_label.setText(f"Page: {self.current_page + 1}")

    def show_begin_page(self):
        self.current_page = 0
        self.populate_table()
        self.update_page_label()

    def show_end_page(self):
        total_pages = (len(self.storing_data) - 1) // self.items_per_page
        self.current_page = total_pages
        self.populate_table()
        self.update_page_label()

    def reload_table(self, new_data: list):
        print("table reload")
        self.table.clearContents()
        self.unique_exams.clear()
        self.current_page = 0
        self.storing_data = new_data
        self.populate_table()
        self.update_page_label()

    def show_previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.populate_table()
            self.update_page_label()

    def show_next_page(self):
        total_pages = (len(self.storing_data) - 1) // self.items_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.populate_table()
            self.update_page_label()

    def populate_table(self):
        data_to_present = self.storing_data[
                          self.current_page * self.items_per_page:(self.current_page + 1) * self.items_per_page]

        for row in range(len(data_to_present)):
            self.table.setRowHeight(row, 93)
            for column in range(self.table.columnCount() - 1):
                item = QTableWidgetItem(data_to_present[row][column])
                self.table.setItem(row, column, item)

            widget = QWidget()
            layout = QVBoxLayout(widget)
            layout.setContentsMargins(0, 0, 0, 0)

            nested_table = QTableWidget()
            nested_table.setRowCount(2)
            nested_table.setColumnCount(3)
            nested_table.setVerticalHeaderLabels(["Наименование дисциплины", "Отметка"])

            for nested_row in range(nested_table.rowCount()):
                for nested_column in range(nested_table.columnCount()):
                    item = QTableWidgetItem(data_to_present[row][-1][nested_column][nested_row])
                    nested_table.setItem(nested_row, nested_column, item)
                    nested_table.setColumnWidth(nested_column, 150)
                    if nested_row == 0:
                        self.unique_exams.add(item.text())

            nested_table.resizeRowsToContents()
            self.table.setColumnWidth(2, 700)
            self.table.setColumnWidth(0, 100)
            self.table.setColumnWidth(1, 100)
            layout.addWidget(nested_table)
            widget.setLayout(layout)

            self.table.setCellWidget(row, self.table.columnCount() - 1, widget)
            self.table.update()


class AddStudentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add Student')
        self.setGeometry(400, 300, 300, 300)
        self.main_window = parent

        self.name_label = QLabel("ФИО:")
        self.name_input = QLineEdit()

        self.group_label = QLabel("Группа (only integer number):")
        self.group_input = QLineEdit()

        self.exam_label = QLabel("Экзамены (exactly 3 and \";\" is a slicer ):")
        self.exam_input = QLineEdit()

        self.exam_marks_label = QLabel("Отметки (for each of the exam):")
        self.exam_marks_input = QLineEdit()

        self.button = QPushButton("Добавить")
        self.button.clicked.connect(self.get_addition_dialog_data)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.group_label)
        layout.addWidget(self.group_input)
        layout.addWidget(self.exam_label)
        layout.addWidget(self.exam_input)
        layout.addWidget(self.exam_marks_label)
        layout.addWidget(self.exam_marks_input)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def get_addition_dialog_data(self):
        name: str = self.name_input.text()
        group: str = self.group_input.text()
        exam_titles: list = self.exam_input.text().split(";")
        exam_marks: list = self.exam_marks_input.text().split(";")
        exams = None
        if name and group and exam_titles != [""] and exam_marks != [""]:
            if len(exam_titles) != len(exam_marks):
                show_warning("amount of exams and marks are not matching")
                self.close()
            else:
                exams = list(zip(exam_titles, exam_marks))
            if len(exams) < 3:
                while len(exams) != 3:
                    show_warning("not enough exams, lacking content will be displayed as\n   \" ( - _ - ) \", \"0\"")
                    exams.append({" ( - _ - ) ", "0"})
            if all(mark.isdigit() for mark in exam_marks):
                if name.isalpha() and group.isdigit() and int(group) > 0 and \
                        all(10 >= int(mark) >= 0 for mark in exam_marks):
                    new_stud_data = [name, group, exams]
                    self.main_window.add_signal.emit(new_stud_data)
                else:
                    show_warning("WRONG INPUTS")
            else:
                show_warning("Marks should be decimal")
        else:
            show_warning("MISSING INPUTS")


class DeleteStudentDialog(QDialog):
    def __init__(self, dialog_type: str, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setGeometry(400, 300, 300, 200)
        if dialog_type == "by_group":
            self.setWindowTitle("Delete student by group")

            self.group_label = QLabel("Группа:")
            self.group_input = QLineEdit()

            self.button = QPushButton("Удалить")
            self.button.clicked.connect(self.delete_student_by_group)

            layout = QVBoxLayout()
            layout.addWidget(self.group_label)
            layout.addWidget(self.group_input)

            layout.addWidget(self.button)

            self.setLayout(layout)

        elif dialog_type == "by_av_mark":
            self.setWindowTitle("Delete student by average mark")

            self.mark_label = QLabel("Средняя отметка")
            self.mark_input = QLineEdit()

            self.button = QPushButton("Удалить")
            self.button.clicked.connect(self.delete_student_by_av_mark)

            layout = QVBoxLayout()
            layout.addWidget(self.mark_label)
            layout.addWidget(self.mark_input)

            layout.addWidget(self.button)

            self.setLayout(layout)

        elif dialog_type == "by_mark_range":
            self.setWindowTitle("Delete student by mark_range")

            self.exam_label = QLabel("Название экзамена")
            self.exam_input = QComboBox()
            for exam in self.main_window.table.unique_exams:
                self.exam_input.addItem(exam)

            self.min_mark_label = QLabel("Минимальная отметка")
            self.min_mark_input = QLineEdit()

            self.max_mark_label = QLabel("Максимальная отметка")
            self.max_mark_input = QLineEdit()

            self.button = QPushButton("Удалить")
            self.button.clicked.connect(self.delete_student_by_mark_range)

            layout = QVBoxLayout()
            layout.addWidget(self.exam_label)
            layout.addWidget(self.exam_input)

            layout.addWidget(self.min_mark_label)
            layout.addWidget(self.min_mark_input)

            layout.addWidget(self.max_mark_label)
            layout.addWidget(self.max_mark_input)

            layout.addWidget(self.button)

            self.setLayout(layout)

    def delete_student_by_group(self):
        group = self.group_input.text()
        if group.isdigit() and int(group) > 0:
            group = int(group)
            self.main_window.del_signal.emit(["by_group", [group]])
            self.close()
        else:
            self.group_input.clear()
            show_warning("WRONG INPUTS")

    def delete_student_by_av_mark(self):
        av_mark = self.mark_input.text()
        if contains_float(av_mark) and 10 >= float(av_mark) >= 0:
            av_mark = float(av_mark)
            self.main_window.del_signal.emit(["by_av_mark", [av_mark]])
            self.close()
        else:
            self.mark_input.clear()
            show_warning("WRONG INPUTS")

    def delete_student_by_mark_range(self):
        exam_index = self.exam_input.currentIndex()
        exam_title = self.exam_input.itemText(exam_index)
        min_mark = self.min_mark_input.text()
        max_mark = self.max_mark_input.text()
        if exam_title and 0 <= int(min_mark) <= int(max_mark) <= 10:
            self.main_window.del_signal.emit(["by_mark_range", [min_mark, max_mark, exam_title]])
            self.close()
        else:
            self.min_mark_input.clear()
            self.max_mark_input.clear()
            show_warning("WRONG INPUTS")


class FindStudentDialog(QDialog):
    def __init__(self, dialog_type: str, parent=None):
        super().__init__(parent)
        print("dialog created")
        self.main_window = parent
        self.setGeometry(500, 230, 1000, 500)
        if dialog_type == "by_group":
            self.setWindowTitle("Find student by group")

            self.table = StudentTable(self.main_window.table.storing_data)
            self.group_input = QLineEdit()
            self.group_input.setPlaceholderText("Группа")

            self.button = QPushButton("Найти")
            self.button.clicked.connect(self.find_student_by_group)

            bottom_layout = QHBoxLayout()
            bottom_layout.addWidget(self.group_input)
            bottom_layout.addWidget(self.button)

            main_layout = QVBoxLayout()
            main_layout.addWidget(self.table)
            main_layout.addLayout(bottom_layout)

            self.setLayout(main_layout)

        elif dialog_type == "by_av_mark":
            self.setWindowTitle("Find student by average mark")

            self.table = StudentTable(self.main_window.table.storing_data)
            self.mark_input = QLineEdit()
            self.mark_input.setPlaceholderText("Средняя отметка")

            self.button = QPushButton("Найти")
            self.button.clicked.connect(self.find_student_by_av_mark)

            bottom_layout = QHBoxLayout()
            bottom_layout.addWidget(self.mark_input)
            bottom_layout.addWidget(self.button)

            main_layout = QVBoxLayout()
            main_layout.addWidget(self.table)
            main_layout.addLayout(bottom_layout)

            self.setLayout(main_layout)

        elif dialog_type == "by_mark_range":
            self.setWindowTitle("Find student by mark range")

            self.table = StudentTable(self.main_window.table.storing_data)
            self.min_input = QLineEdit()
            self.min_input.setPlaceholderText("Минимальная отметка")

            self.max_input = QLineEdit()
            self.max_input.setPlaceholderText("Максимальная отметка")

            self.title_input = QComboBox()
            for exam in self.main_window.table.unique_exams:
                self.title_input.addItem(exam)

            self.button = QPushButton("Найти")
            self.button.clicked.connect(self.find_student_by_mark_range)

            bottom_layout = QHBoxLayout()
            bottom_layout.addWidget(self.min_input)
            bottom_layout.addWidget(self.max_input)
            bottom_layout.addWidget(self.title_input)
            bottom_layout.addWidget(self.button)
            main_layout = QVBoxLayout()
            main_layout.addWidget(self.table)
            main_layout.addLayout(bottom_layout)

            self.setLayout(main_layout)

    def update_table_with_new_data(self, new_data):
        print("updating data")
        self.table.reload_table(new_data)

    def find_student_by_group(self):
        group = self.group_input.text()
        self.group_input.clear()
        if group.isdigit():
            group = int(group)
            self.main_window.find_signal.emit(["by_group", [group]])
        else:
            show_warning("WRONG INPUTS")

    def find_student_by_av_mark(self):
        av_mark = self.mark_input.text()
        self.mark_input.clear()
        if contains_float(av_mark):
            av_mark = float(av_mark)
            self.main_window.find_signal.emit(["by_av_mark", [av_mark]])
        else:
            show_warning("WRONG INPUTS")

    def find_student_by_mark_range(self):
        exam_index = self.title_input.currentIndex()
        exam_title = self.title_input.itemText(exam_index)
        min_mark = self.min_input.text()
        max_mark = self.max_input.text()
        self.max_input.clear()
        self.min_input.clear()

        if exam_title and min_mark.isdigit() and max_mark.isdigit() and 0 <= int(min_mark) <= int(max_mark) <= 10:
            self.main_window.find_signal.emit(["by_mark_range", [min_mark, max_mark, exam_title]])
        else:
            show_warning("WRONG INPUTS")


class MainWindow(QMainWindow):
    add_signal = pyqtSignal(list)
    del_signal = pyqtSignal(list)
    find_signal = pyqtSignal(list)
    retrieve_signal = pyqtSignal(list)
    save_file_signal = pyqtSignal(str)
    open_signal = pyqtSignal(str)
    def __init__(self, _data: list):
        super().__init__()
        self.setWindowTitle('STUDENTS')
        self.setGeometry(460, 200, 1000, 500)
        self.find_ref = None

        add_action = QAction("ADD", self)
        add_action.triggered.connect(self.addition_dialog)
        self.menuBar().addAction(add_action)

        delete_by_group = QAction("By group", self)
        delete_by_av_mark = QAction("By average marks", self)
        delete_by_mark_range = QAction("By mark range", self)

        delete_by_mark_range.triggered.connect(lambda: self.deletion_dialog("by_mark_range"))
        delete_by_group.triggered.connect(lambda: self.deletion_dialog("by_group"))
        delete_by_av_mark.triggered.connect(lambda: self.deletion_dialog("by_av_mark"))

        del_menu = self.menuBar()
        menu_del = del_menu.addMenu("DELETE")
        menu_del.addAction(delete_by_group)
        menu_del.addAction(delete_by_av_mark)
        menu_del.addAction(delete_by_mark_range)

        find_by_group = QAction("By group", self)
        find_by_av_mark = QAction("By average marks", self)
        find_by_mark_range = QAction("By mark range", self)

        find_by_mark_range.triggered.connect(lambda: self.find_dialog("by_mark_range"))
        find_by_group.triggered.connect(lambda: self.find_dialog("by_group"))
        find_by_av_mark.triggered.connect(lambda: self.find_dialog("by_av_mark"))

        find_menu = self.menuBar()
        menu_find = find_menu.addMenu("FIND")
        menu_find.addAction(find_by_group)
        menu_find.addAction(find_by_av_mark)
        menu_find.addAction(find_by_mark_range)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('FILE')
        save_as_action = QAction('Save As', self)
        save_as_action.triggered.connect(self.save_as)
        open_as_action = QAction('Open', self)
        open_as_action.triggered.connect(self.open_file)
        file_menu.addAction(open_as_action)
        file_menu.addAction(save_as_action)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.table = StudentTable(_data)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(self.table)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(None, "Open File", "", "*.xml")
        self.open_signal.emit(filename)
    def save_as(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save File As", "", "All Files (*);;Text Files (*.txt);;XML(*.xml)", options=options
        )
        if file_name:
            self.save_file_signal.emit(file_name)


    def addition_dialog(self):
        dialog = AddStudentDialog(self)
        dialog.exec_()

    def deletion_dialog(self, dialog_type: str):
        dialog = DeleteStudentDialog(dialog_type, self)
        dialog.exec_()

    def find_dialog(self, dialog_type: str):
        find_dialog = FindStudentDialog(dialog_type, self)
        self.retrieve_signal.connect(find_dialog.update_table_with_new_data)
        find_dialog.exec_()


if __name__ == '__main__':
    data = [
        ["John Doe", "Group A", [["Math", "A"], ["Physics", "B"], ["Physics", "B"]]],
        ["Jane Smith", "Group B", [["Chemistry", "C"], ["Biology", "A"], ["Physics", "B"]]],
        ["Bob Johnson", "Group A", [["English", "B"], ["History", "A"], ["Physics", "B"]]],
        ["Emily Davis", "Group C", [["Geography", "C"], ["Art", "B"], ["Physics", "B"]]],
        ["Michael Wilson", "Group B", [["Computer Science", "A"], ["Music", "B"], ["Physics", "B"]]],
        ["Jo Doe", "Gro A", [["Math", "A"], ["Physics", "B"], ["Physics", "B"]]],
        ["ne Smith", "Gro B", [["Chemistry", "C"], ["Biology", "A"], ["Physics", "B"]]],
        ["b Johnson", "Gro A", [["English", "B"], ["History", "A"], ["Physics", "B"]]],
        ["ily Davis", "Gro C", [["Geography", "C"], ["Art", "B"], ["Physics", "B"]]],
        ["chael Wilson", "Gro B", [["Computer Science", "A"], ["Music", "B"], ["Physics", "B"]]],
    ]

    app = QApplication(sys.argv)
    window = MainWindow(data)
    window.add_signal.connect(print)
    window.show()

    sys.exit(app.exec_())
