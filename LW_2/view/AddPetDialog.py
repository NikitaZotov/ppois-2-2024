import re

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox


class AddPetDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Pet")
        self.setFixedSize(400, 300)

        layout = QtWidgets.QVBoxLayout()

        self.name_edit = QtWidgets.QLineEdit()
        self.name_edit.setPlaceholderText("Pet's name")
        self.name_edit.setFont(QtGui.QFont("Times New Roman", 12))
        layout.addWidget(self.name_edit)

        # Дата рождения
        birth_date_label = QtWidgets.QLabel("Date of Birth:")
        birth_date_label.setFont(QtGui.QFont("Times New Roman", 12))
        layout.addWidget(birth_date_label)
        self.birth_date_edit = QtWidgets.QDateEdit()
        self.birth_date_edit.setStyleSheet("font: 12pt 'Times New Roman'")
        self.birth_date_edit.setCalendarPopup(True)
        self.birth_date_edit.setDate(QtCore.QDate.currentDate())
        layout.addWidget(self.birth_date_edit)

        # Последний визит
        last_appointment_label = QtWidgets.QLabel("Last Appointment:")
        last_appointment_label.setFont(QtGui.QFont("Times New Roman", 12))
        layout.addWidget(last_appointment_label)
        self.last_appointment_edit = QtWidgets.QDateEdit()
        self.last_appointment_edit.setStyleSheet("font: 12pt 'Times New Roman'")
        self.last_appointment_edit.setCalendarPopup(True)
        self.last_appointment_edit.setDate(QtCore.QDate.currentDate())
        layout.addWidget(self.last_appointment_edit)

        self.veterinarian_edit = QtWidgets.QLineEdit()
        self.veterinarian_edit.setPlaceholderText("Veterinarian")
        self.veterinarian_edit.setFont(QtGui.QFont("Times New Roman", 12))
        layout.addWidget(self.veterinarian_edit)

        self.diagnosis_edit = QtWidgets.QLineEdit()
        self.diagnosis_edit.setPlaceholderText("Diagnosis")
        self.diagnosis_edit.setFont(QtGui.QFont("Times New Roman", 12))
        layout.addWidget(self.diagnosis_edit)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_pet_info(self):
        while True:
            name = self.name_edit.text().strip()  # Убираем лишние пробелы в начале и конце
            if not name:
                QMessageBox.warning(self, "Warning", "Please enter the pet's name.")
                return None
            if not name.isalpha():
                QMessageBox.warning(None, "Warning", "Name should only contain letters of the Latin alphabet.")
                return
            if re.search(r'\d', name):
                QMessageBox.warning(None, "Warning", "Name should only contain letters of the Latin alphabet.")
                return
            birth_date = self.birth_date_edit.date().toString(QtCore.Qt.ISODate)
            last_appointment = self.last_appointment_edit.date().toString(QtCore.Qt.ISODate)
            if last_appointment < birth_date:
                QMessageBox.warning(None, "Warning", "Date of last appointment cannot be before date of birth.")
                return
            veterinarian = self.veterinarian_edit.text().strip()
            if not veterinarian:
                QMessageBox.warning(self, "Warning", "Please enter the veterinarian's name.")
                return None
            if not veterinarian.isalpha():
                QMessageBox.warning(None, "Warning", "Surname should only contain letters of the Latin alphabet.")
                return
            if re.search(r'\d', veterinarian):
                QMessageBox.warning(None, "Warning", "Surname should only contain letters of the Latin alphabet.")
                return
            diagnosis = self.diagnosis_edit.text().strip()
            if not diagnosis:
                QMessageBox.warning(self, "Warning", "Please enter the diagnosis.")
                return None
            if not diagnosis.isalpha():
                QMessageBox.warning(None, "Warning", "Diagnosis should only contain letters of the Latin alphabet.")
                return
            if re.search(r'\d', diagnosis):
                QMessageBox.warning(None, "Warning", "Diagnosis should only contain letters of the Latin alphabet.")
                return
            return name, birth_date, last_appointment, veterinarian, diagnosis