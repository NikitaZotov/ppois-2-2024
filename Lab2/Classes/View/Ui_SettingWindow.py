from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SettingWindow():
    def setupUi(self, MainWindow, index):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(370, 180)
        MainWindow.setMaximumSize(QtCore.QSize(370, 180))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mainLabel = QtWidgets.QLabel(self.centralwidget)
        self.mainLabel.setGeometry(QtCore.QRect(90, 10, 180, 50))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.mainLabel.setFont(font)
        self.mainLabel.setObjectName("mainLabel")
        self.comboBoxCountInPage = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxCountInPage.setGeometry(QtCore.QRect(320, 80, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.comboBoxCountInPage.setFont(font)
        self.comboBoxCountInPage.setObjectName("comboBoxCountInPage")
        self.comboBoxCountInPage.addItem("")
        self.comboBoxCountInPage.addItem("")
        self.comboBoxCountInPage.addItem("")
        self.comboBoxCountInPage.addItem("")
        self.comboBoxCountInPage.setCurrentIndex(index)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 80, 301, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.btnSave = QtWidgets.QPushButton(self.centralwidget)
        self.btnSave.setGeometry(QtCore.QRect(135, 130, 100, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnSave.setFont(font)
        self.btnSave.setObjectName("btnSave")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Настройки"))
        self.mainLabel.setText(_translate("MainWindow", "Настройки"))
        self.comboBoxCountInPage.setItemText(0, _translate("MainWindow", "5"))
        self.comboBoxCountInPage.setItemText(1, _translate("MainWindow", "8"))
        self.comboBoxCountInPage.setItemText(2, _translate("MainWindow", "10"))
        self.comboBoxCountInPage.setItemText(3, _translate("MainWindow", "15"))
        self.label.setText(_translate("MainWindow", "Количество записей на одной странице"))
        self.btnSave.setText(_translate("MainWindow", "Сохранить"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_SettingWindow()
    ui.setupUi(MainWindow, 1)
    MainWindow.show()
    sys.exit(app.exec_())
