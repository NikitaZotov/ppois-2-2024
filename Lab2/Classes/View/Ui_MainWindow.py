from PyQt5 import QtCore, QtGui, QtWidgets
#import sys

class Ui_MainWindow:
    def __init__(self):
        self._count_of_records_in_page = 8
        self._count_of_pages = 1
        self._count_of_records_on_last_page = 0
        self._size_of_item = 40
        self._size_of_font = 12

    @property
    def count_of_records_in_page(self):
        return self._count_of_records_in_page

    @count_of_records_in_page.setter
    def count_of_records_in_page(self, value):
        self._count_of_records_in_page = value

    @property
    def count_of_pages(self):
        return self._count_of_pages

    @count_of_pages.setter
    def count_of_pages(self, count):
        self._count_of_pages = count

    @property
    def count_of_records_on_last_page(self):
        return self._count_of_records_on_last_page

    @count_of_records_on_last_page.setter
    def count_of_records_on_last_page(self, count):
        self._count_of_records_on_last_page = count

    @property
    def size_of_item(self):
        return self._size_of_item

    @size_of_item.setter
    def size_of_item(self, size):
        self._size_of_item = size

    @property
    def size_of_font(self):
        return self._size_of_font

    @size_of_font.setter
    def size_of_font(self, size):
        self._size_of_font = size

    def setupUi(self, MainWindow, list_of_trains):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1140, 550)
        MainWindow.setMaximumSize(QtCore.QSize(1160, 550))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Title = QtWidgets.QLabel(self.centralwidget)
        self.Title.setGeometry(QtCore.QRect(10, 10, 411, 41))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.Title.setFont(font)
        self.Title.setObjectName("Title")
        self.AddTrain = QtWidgets.QPushButton(self.centralwidget)
        self.AddTrain.setGeometry(QtCore.QRect(1010, 20, 35, 35))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.AddTrain.setFont(font)
        self.AddTrain.setStyleSheet("color: rgb(0, 212, 0);\n""")
        self.AddTrain.setObjectName("AddTrain")
        self.RemoveTrain = QtWidgets.QPushButton(self.centralwidget)
        self.RemoveTrain.setGeometry(QtCore.QRect(1050, 20, 35, 35))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.RemoveTrain.setFont(font)
        self.RemoveTrain.setStyleSheet("color: rgb(206, 0, 0);")
        self.RemoveTrain.setObjectName("RemoveTrain")
        self.FindTrain = QtWidgets.QPushButton(self.centralwidget)
        self.FindTrain.setGeometry(QtCore.QRect(1090, 20, 35, 35))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.FindTrain.setFont(font)
        self.FindTrain.setStyleSheet("")
        self.FindTrain.setObjectName("FindTrain")
        self.Save = QtWidgets.QPushButton(self.centralwidget)
        self.Save.setGeometry(QtCore.QRect(1010, 460, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Save.setFont(font)
        self.Save.setObjectName("Save")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 60, 1121, 390))
        self.tabWidget.setObjectName("tabWidget")

        for index in range (0, self._count_of_pages):
            self.Page = QtWidgets.QWidget()
            self.Page.setObjectName("Page1")
            self.Table = QtWidgets.QTableWidget(self.Page)
            self.Table.setGeometry(QtCore.QRect(0, 0, 1122, 370))
            font = QtGui.QFont()
            font.setPointSize(self._size_of_font)
            self.Table.setFont(font)
            self.Table.setMouseTracking(False)
            self.Table.setTabletTracking(False)
            self.Table.setToolTip("")
            self.Table.setStatusTip("")
            self.Table.setWhatsThis("")
            self.Table.setAccessibleName("")
            self.Table.setInputMethodHints(QtCore.Qt.ImhNone)
            self.Table.setAutoScroll(False)
            self.Table.setAutoScrollMargin(10)
            self.Table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.Table.setTabKeyNavigation(True)
            self.Table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
            self.Table.setObjectName("Table")
            self.Table.setColumnCount(8)
            if index == self._count_of_pages - 1:
                self.Table.setRowCount(self._count_of_records_on_last_page)
                for i in range(0, self._count_of_records_on_last_page):
                    item = QtWidgets.QTableWidgetItem()
                    self.Table.setVerticalHeaderItem(i, item)

            else:
                self.Table.setRowCount(self._count_of_records_in_page)
                for i in range(0, self._count_of_records_in_page):
                    item = QtWidgets.QTableWidgetItem()
                    self.Table.setVerticalHeaderItem(i, item)

            item = QtWidgets.QTableWidgetItem()
            self.Table.setHorizontalHeaderItem(0, item)
            item = QtWidgets.QTableWidgetItem()
            self.Table.setHorizontalHeaderItem(1, item)
            item = QtWidgets.QTableWidgetItem()
            self.Table.setHorizontalHeaderItem(2, item)
            item = QtWidgets.QTableWidgetItem()
            self.Table.setHorizontalHeaderItem(3, item)
            item = QtWidgets.QTableWidgetItem()
            self.Table.setHorizontalHeaderItem(4, item)
            item = QtWidgets.QTableWidgetItem()
            self.Table.setHorizontalHeaderItem(5, item)
            item = QtWidgets.QTableWidgetItem()
            self.Table.setHorizontalHeaderItem(6, item)
            item = QtWidgets.QTableWidgetItem()
            self.Table.setHorizontalHeaderItem(7, item)
            if index == self._count_of_pages - 1:
                for j in range(0, 8):
                    for i in range(0, self._count_of_records_on_last_page):
                        item = QtWidgets.QTableWidgetItem()
                        self.Table.setItem(i, j, item)

            else:
                for j in range(0, 8):
                    for i in range(0, self._count_of_records_in_page):
                        item = QtWidgets.QTableWidgetItem()
                        self.Table.setItem(i, j, item)

            self.Table.horizontalHeader().setVisible(True)
            self.Table.horizontalHeader().setCascadingSectionResizes(True)
            self.Table.horizontalHeader().setDefaultSectionSize(140)
            self.Table.horizontalHeader().setHighlightSections(True)
            self.Table.horizontalHeader().setMinimumSectionSize(49)
            self.Table.verticalHeader().setVisible(False)
            self.Table.verticalHeader().setDefaultSectionSize(self._size_of_item)
            self.Table.verticalHeader().setMinimumSectionSize(10)
            self.tabWidget.addTab(self.Page, "")
            if index == self._count_of_pages - 1:
                self.retranslateUi_table(index, self._count_of_records_on_last_page, index * self._count_of_records_in_page, list_of_trains)
            else:
                self.retranslateUi_table(index, self._count_of_records_in_page,index * self._count_of_records_in_page, list_of_trains)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1140, 21))
        self.menubar.setObjectName("menubar")
        self.FileMenu = QtWidgets.QMenu(self.menubar)
        self.FileMenu.setObjectName("FileMenu")
        self.Edit = QtWidgets.QMenu(self.menubar)
        self.Edit.setObjectName("EditMenu")
        self.Display = QtWidgets.QMenu(self.menubar)
        self.Display.setObjectName("DisplayMenu")
        MainWindow.setMenuBar(self.menubar)
        self.OpenMenu = QtWidgets.QAction(MainWindow)
        self.OpenMenu.setObjectName("OpenMenu")
        self.SaveMenu = QtWidgets.QAction(MainWindow)
        self.SaveMenu.setObjectName("SaveMenu")
        self.ClearMenu = QtWidgets.QAction(MainWindow)
        self.ClearMenu.setObjectName("ClearMenu")
        self.AddRecordMenu = QtWidgets.QAction(MainWindow)
        self.AddRecordMenu.setObjectName("AddRecordMenu")
        self.RemoveRecordMenu = QtWidgets.QAction(MainWindow)
        self.RemoveRecordMenu.setObjectName("RemoveRecordMenu")
        self.FindRecordMenu = QtWidgets.QAction(MainWindow)
        self.FindRecordMenu.setObjectName("FindRecordMenu")
        self.SettingMenu = QtWidgets.QAction(MainWindow)
        self.SettingMenu.setObjectName("SettingMenu")
        self.FileMenu.addAction(self.OpenMenu)
        self.FileMenu.addAction(self.SaveMenu)
        self.FileMenu.addAction(self.ClearMenu)
        self.Edit.addAction(self.AddRecordMenu)
        self.Edit.addAction(self.RemoveRecordMenu)
        self.Edit.addAction(self.FindRecordMenu)
        self.Display.addAction(self.SettingMenu)
        self.menubar.addAction(self.FileMenu.menuAction())
        self.menubar.addAction(self.Edit.menuAction())
        self.menubar.addAction(self.Display.menuAction())

        self.retranslateUi_menu(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi_table(self, number_of_page, count_of_records_in_page, first_index_record, list_of_trains):

        _translate = QtCore.QCoreApplication.translate

        item = self.Table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Номер поезда"))
        item = self.Table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Ст. отправления"))
        item = self.Table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Ст. прибытия"))
        item = self.Table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Дата оправления"))
        item = self.Table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Время оправления"))
        item = self.Table.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Дата прибытия"))
        item = self.Table.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Время прибытия"))
        item = self.Table.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Время в пути"))
        __sortingEnabled = self.Table.isSortingEnabled()
        self.Table.setSortingEnabled(False)
        for index in range(0, count_of_records_in_page):
            item = self.Table.item(index, 0)
            item.setText(_translate("MainWindow", list_of_trains[index + first_index_record].number_of_train))
            item = self.Table.item(index, 1)
            item.setText(_translate("MainWindow", list_of_trains[index + first_index_record].first_station))
            item = self.Table.item(index, 2)
            item.setText(_translate("MainWindow", list_of_trains[index + first_index_record].last_station))
            item = self.Table.item(index, 3)
            item.setText(_translate("MainWindow", list_of_trains[index + first_index_record].departure_date))
            item = self.Table.item(index, 4)
            item.setText(_translate("MainWindow", list_of_trains[index + first_index_record].departure_time))
            item = self.Table.item(index, 5)
            item.setText(_translate("MainWindow", list_of_trains[index + first_index_record].arrival_date))
            item = self.Table.item(index, 6)
            item.setText(_translate("MainWindow", list_of_trains[index + first_index_record].arrival_time))
            item = self.Table.item(index, 7)
            item.setText(_translate("MainWindow", str(list_of_trains[index + first_index_record].travel_time)))

        self.Table.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Page), _translate("MainWindow", "Страница " + str(number_of_page + 1)))


    def retranslateUi_menu(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Расписание поездов"))
        self.Title.setText(_translate("MainWindow", "Расписание поездов"))
        self.AddTrain.setText(_translate("MainWindow", "+"))
        self.RemoveTrain.setText(_translate("MainWindow", "-"))
        self.FindTrain.setText(_translate("MainWindow", "?"))
        self.Save.setText(_translate("MainWindow", "Сохранить"))
        self.FileMenu.setTitle(_translate("MainWindow", "Файл"))
        self.Edit.setTitle(_translate("MainWindow", "Редактирование"))
        self.Display.setTitle(_translate("MainWindow", "Вид"))
        self.AddRecordMenu.setText(_translate("MainWindow", "Добавить запись"))
        self.AddRecordMenu.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.RemoveRecordMenu.setText(_translate("MainWindow", "Удалить запись"))
        self.RemoveRecordMenu.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.FindRecordMenu.setText(_translate("MainWindow", "Поиск"))
        self.FindRecordMenu.setShortcut(_translate("MainWindow", "Ctrl+F"))
        self.SettingMenu.setText(_translate("MainWindow", "Настройки"))
        self.OpenMenu.setText(_translate("MainWindow", "Открыть"))
        self.OpenMenu.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.SaveMenu.setText(_translate("MainWindow", "Сохранить"))
        self.SaveMenu.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.ClearMenu.setText(_translate("MainWindow", "Очистить"))
        self.ClearMenu.setShortcut(_translate("MainWindow", "Ctrl+Q"))