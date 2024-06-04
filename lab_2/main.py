import sys
from PyQt5.QtWidgets import QApplication
from model import ProductModel
from views import MainWindow

def main():
    app = QApplication(sys.argv)
    model = ProductModel()
    main_window = MainWindow(model)
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
