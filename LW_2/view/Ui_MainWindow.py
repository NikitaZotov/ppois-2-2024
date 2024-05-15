import re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
 # Можно создавать всплывающие окна


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.records = []
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(832, 699)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_create_file = QtWidgets.QPushButton(self.centralwidget)
        self.btn_create_file.setGeometry(QtCore.QRect(20, 20, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_create_file.setFont(font)
        self.btn_create_file.setStyleSheet("background-color: rgb(85, 170, 0);\n"
"border-color: rgb(0, 0, 0);\n"
"")
        self.btn_create_file.setObjectName("btn_create_file")
        self.btn_open_file = QtWidgets.QPushButton(self.centralwidget)
        self.btn_open_file.setGeometry(QtCore.QRect(140, 20, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setBold(True)
        font.setWeight(75)
        self.btn_open_file.setFont(font)
        self.btn_open_file.setStyleSheet("background-color: rgb(85, 170, 0);\n"
"border-color: rgb(0, 0, 0);\n"
"")
        self.btn_open_file.setObjectName("btn_open_file")
        self.btn_add_pet = QtWidgets.QPushButton(self.centralwidget)
        self.btn_add_pet.setGeometry(QtCore.QRect(260, 20, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setBold(True)
        font.setWeight(75)
        self.btn_add_pet.setFont(font)
        self.btn_add_pet.setStyleSheet("background-color: rgb(85, 170, 0);\n"
"border-color: rgb(0, 0, 0);\n"
"")
        self.btn_add_pet.setObjectName("btn_add_pet")
        self.btn_search_by_filter = QtWidgets.QPushButton(self.centralwidget)
        self.btn_search_by_filter.setGeometry(QtCore.QRect(380, 20, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_search_by_filter.setFont(font)
        self.btn_search_by_filter.setStyleSheet("background-color: rgb(85, 170, 0);\n"
"border-color: rgb(0, 0, 0);\n"
"")
        self.btn_search_by_filter.setObjectName("btn_search_by_filter")
        self.btn_delete_by_filter = QtWidgets.QPushButton(self.centralwidget)
        self.btn_delete_by_filter.setGeometry(QtCore.QRect(530, 20, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_delete_by_filter.setFont(font)
        self.btn_delete_by_filter.setStyleSheet("background-color: rgb(255, 0, 0);\n"
"border-color: rgb(0, 0, 0);\n"
"")
        self.btn_delete_by_filter.setObjectName("btn_delete_by_filter")
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setEnabled(True)
        self.table.setGeometry(QtCore.QRect(20, 70, 790, 490))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setUnderline(False)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.table.setFont(font)
        self.table.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.table.setAutoFillBackground(False)
        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.table.setObjectName("table")
        self.table.setColumnCount(5)
        self.table.setRowCount(10)
        item = QtWidgets.QTableWidgetItem()
        self.table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table.setHorizontalHeaderItem(4, item)
        self.table.horizontalHeader().setCascadingSectionResizes(True)
        self.table.horizontalHeader().setDefaultSectionSize(152)
        self.table.horizontalHeader().setMinimumSectionSize(49)
        self.table.verticalHeader().setDefaultSectionSize(46)
        self.btn_prev_page = QtWidgets.QPushButton(self.centralwidget)
        self.btn_prev_page.setGeometry(QtCore.QRect(550, 590, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.btn_prev_page.setFont(font)
        self.btn_prev_page.setStyleSheet("background-color: rgb(172, 172, 172);\n"
"border-color: rgb(0, 0, 0);")
        self.btn_prev_page.setObjectName("btn_prev_page")
        self.btn_next_page = QtWidgets.QPushButton(self.centralwidget)
        self.btn_next_page.setGeometry(QtCore.QRect(670, 590, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.btn_next_page.setFont(font)
        self.btn_next_page.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-color: rgb(0, 0, 0);")
        self.btn_next_page.setObjectName("btn_next_page")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(260, 590, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.spinBox.setFont(font)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(10)
        self.spinBox.setValue(10)
        self.spinBox.setObjectName("spinBox")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 590, 225, 31))
        self.textEdit.setObjectName("textEdit")
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.textEdit.setFont(font)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 832, 29))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.btn_first_page = QtWidgets.QPushButton(self.centralwidget)
        self.btn_first_page.setGeometry(QtCore.QRect(550, 640, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.btn_first_page.setFont(font)
        self.btn_first_page.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                          "border-color: rgb(0, 0, 0);")
        self.btn_first_page.setObjectName("btn_first_page")
        self.btn_first_page.setText("First Page")
        self.btn_last_page = QtWidgets.QPushButton(self.centralwidget)
        self.btn_last_page.setGeometry(QtCore.QRect(670, 640, 93, 28))
        self.btn_last_page.setFont(font)
        self.btn_last_page.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                         "border-color: rgb(0, 0, 0);")
        self.btn_last_page.setObjectName("btn_last_page")
        self.btn_last_page.setText("Last Page")

        self.label_total_entries = QtWidgets.QTextEdit(self.centralwidget)
        self.label_total_entries.setGeometry(QtCore.QRect(20, 640, 225, 31))
        self.label_total_entries.setObjectName("label_total_entries")
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.label_total_entries.setFont(font)
        self.label_total_entries.setPlainText("Entries 0/0. Total entries: 0")

        self.disable_table_editing()
        self.page_size = 10
        self.current_page = 1
        self.total_pages = 1

        self.btn_return_to_initial = QtWidgets.QPushButton(self.centralwidget)
        self.btn_return_to_initial.setGeometry(QtCore.QRect(690, 20, 93, 31))
        self.btn_return_to_initial.setFont(font)
        self.btn_return_to_initial.setObjectName("btn_return_to_initial")
        self.btn_return_to_initial.setText("Return")
        self.btn_return_to_initial.setVisible(False)

        self.disable_page_navigation()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def disable_table_editing(self):
            self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def disable_page_navigation(self):
            if not self.records:
                self.btn_prev_page.setEnabled(False)
                self.btn_next_page.setEnabled(False)
                self.btn_first_page.setEnabled(False)
                self.btn_last_page.setEnabled(False)
                self.spinBox.setEnabled(False)

    def enable_page_navigation(self):
        self.btn_prev_page.setEnabled(True)
        self.btn_next_page.setEnabled(True)
        self.btn_first_page.setEnabled(True)
        self.btn_last_page.setEnabled(True)
        self.spinBox.setEnabled(True)

    def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "Veterinary clinic"))
            self.btn_create_file.setText(_translate("MainWindow", "Create file"))
            self.btn_open_file.setText(_translate("MainWindow", "Open file"))
            self.btn_add_pet.setText(_translate("MainWindow", "Add pet"))
            self.btn_search_by_filter.setText(_translate("MainWindow", "Search by filter"))
            self.btn_delete_by_filter.setText(_translate("MainWindow", "Delete by filter"))
            item = self.table.verticalHeaderItem(0)
            item.setText(_translate("MainWindow", "1"))
            item = self.table.verticalHeaderItem(1)
            item.setText(_translate("MainWindow", "2"))
            item = self.table.verticalHeaderItem(2)
            item.setText(_translate("MainWindow", "3"))
            item = self.table.verticalHeaderItem(3)
            item.setText(_translate("MainWindow", "4"))
            item = self.table.verticalHeaderItem(4)
            item.setText(_translate("MainWindow", "5"))
            item = self.table.horizontalHeaderItem(0)
            item.setText(_translate("MainWindow", "Pet\'s name"))
            item = self.table.horizontalHeaderItem(1)
            item.setText(_translate("MainWindow", "Date of birth"))
            item = self.table.horizontalHeaderItem(2)
            item.setText(_translate("MainWindow", "Last appointment"))
            item = self.table.horizontalHeaderItem(3)
            item.setText(_translate("MainWindow", "Veterinarian"))
            item = self.table.horizontalHeaderItem(4)
            item.setText(_translate("MainWindow", "Diagnosis"))
            __sortingEnabled = self.table.isSortingEnabled()
            self.table.setSortingEnabled(False)

            self.btn_prev_page.setText(_translate("MainWindow", "Prev Page"))
            self.btn_next_page.setText(_translate("MainWindow", "Next Page"))
            self.textEdit.setText(_translate("MainWindow", "Page 1/1. Entries on page:"))

    def show_records(self, pets):
        self.clear_table()
        # Отображаем записи на текущей странице
        start_index = (self.current_page - 1) * self.page_size
        end_index = min(start_index + self.page_size, len(pets))

        for i, pet in enumerate(pets[start_index:end_index]):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(pet.pets_name))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(pet.date_of_birth))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(pet.last_appointment))
            self.table.setItem(i, 3, QtWidgets.QTableWidgetItem(pet.veterinarian))
            self.table.setItem(i, 4, QtWidgets.QTableWidgetItem(pet.diagnosis))

        # Обновляем информацию о текущей странице и количестве страниц
        self.textEdit.setPlainText(f"Page {self.current_page}/{self.total_pages}. Entries on page:")

        self.label_total_entries.setPlainText(
            f"Entries {end_index - start_index}/{self.page_size}.Total entries: {len(pets)}")
        self.enable_page_navigation()

    def clear_table(self):
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = QtWidgets.QTableWidgetItem()
                self.table.setItem(row, col, item)











