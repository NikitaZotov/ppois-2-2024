from PyQt5 import QtWidgets

class MessageWindow(QtWidgets.QMainWindow):

    @staticmethod
    def show_information_message(informative_text):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle("Информация")
        msg.setText("Данное окно было закрыто")
        msg.setInformativeText(informative_text)
        msg.exec_()

    @staticmethod
    def show_error_message(error_text):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowTitle("Ошибка")
        msg.setText("Некорректный ввод данных")
        msg.setStandardButtons(QtWidgets.QMessageBox.Cancel)
        msg.setInformativeText(error_text)
        msg.exec_()
