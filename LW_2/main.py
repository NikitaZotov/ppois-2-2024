from PyQt5 import QtWidgets
from model.PetModel import PetModel
from controller.Controller import PetController
from view.Ui_MainWindow import Ui_MainWindow

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    model = PetModel()
    controller = PetController(model, ui)

    MainWindow.show()
    sys.exit(app.exec_())