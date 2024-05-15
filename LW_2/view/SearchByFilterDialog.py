from PyQt5 import QtWidgets

class SearchByFilterDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Search by filter")
        self.setFixedSize(471, 440)

        layout = QtWidgets.QVBoxLayout()

        self.group = QtWidgets.QButtonGroup(self)
        self.group.setExclusive(True)

        self.checkBox_phrase_diagnosis = QtWidgets.QCheckBox("by the phrase from the diagnosis")
        self.checkBox_phrase_diagnosis.toggled.connect(lambda: self.toggle_group(self.checkBox_phrase_diagnosis))
        layout.addWidget(self.checkBox_phrase_diagnosis)
        self.group.addButton(self.checkBox_phrase_diagnosis)

        self.checkBox_by_pet_and_dob = QtWidgets.QCheckBox("by pet's name and date of birth")
        self.checkBox_by_pet_and_dob.toggled.connect(lambda: self.toggle_group(self.checkBox_by_pet_and_dob))
        layout.addWidget(self.checkBox_by_pet_and_dob)
        self.group.addButton(self.checkBox_by_pet_and_dob)

        self.checkBox_last_appoit_and_vet = QtWidgets.QCheckBox("by the date of the last appointment and the name of the veterinarian")
        self.checkBox_last_appoit_and_vet.toggled.connect(lambda: self.toggle_group(self.checkBox_last_appoit_and_vet))
        layout.addWidget(self.checkBox_last_appoit_and_vet)
        self.group.addButton(self.checkBox_last_appoit_and_vet)

        self.line_pet_name = QtWidgets.QLineEdit()
        self.line_pet_name.setPlaceholderText("Pet's name")
        self.line_pet_name.setEnabled(False)  # Initially disabled
        layout.addWidget(self.line_pet_name)

        self.line_veterinar = QtWidgets.QLineEdit()
        self.line_veterinar.setPlaceholderText("Name of the veterinarian")
        self.line_veterinar.setEnabled(False)  # Initially disabled
        layout.addWidget(self.line_veterinar)

        self.line_dob = QtWidgets.QLineEdit()
        self.line_dob.setPlaceholderText("Date of birth")
        self.line_dob.setEnabled(False)  # Initially disabled
        layout.addWidget(self.line_dob)

        self.line_last_appoit = QtWidgets.QLineEdit()
        self.line_last_appoit.setPlaceholderText("Date of the last appoitment")
        self.line_last_appoit.setEnabled(False)  # Initially disabled
        layout.addWidget(self.line_last_appoit)

        self.line_phrase = QtWidgets.QLineEdit()
        self.line_phrase.setPlaceholderText("The prase from the diagnosis")
        self.line_phrase.setEnabled(False)  # Initially disabled
        layout.addWidget(self.line_phrase)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def toggle_group(self, selected):
        for button in self.group.buttons():
            if button is not selected:
                button.setChecked(False)

        # Enable/disable corresponding line edits based on selected checkbox
        if selected == self.checkBox_phrase_diagnosis:
            self.line_phrase.setEnabled(selected.isChecked())
        elif selected == self.checkBox_by_pet_and_dob:
            self.line_pet_name.setEnabled(selected.isChecked())
            self.line_dob.setEnabled(selected.isChecked())
        elif selected == self.checkBox_last_appoit_and_vet:
            self.line_last_appoit.setEnabled(selected.isChecked())
            self.line_veterinar.setEnabled(selected.isChecked())

    def get_search_criteria(self):
        criteria = {}
        if self.checkBox_phrase_diagnosis.isChecked():
            criteria['phrase_diagnosis'] = self.line_phrase.text()
        if self.checkBox_by_pet_and_dob.isChecked():
            criteria['pet_name'] = self.line_pet_name.text()
            criteria['dob'] = self.line_dob.text()
        if self.checkBox_last_appoit_and_vet.isChecked():
            criteria['last_appointment'] = self.line_last_appoit.text()
            criteria['veterinarian'] = self.line_veterinar.text()
        return criteria