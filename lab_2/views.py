from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QComboBox, QFileDialog,  QTableWidget, QTableWidgetItem
)
from PyQt5.QtWidgets import (
     QMainWindow, QVBoxLayout, QPushButton, QComboBox, QFileDialog, QWidget
)
from PyQt5.QtWidgets import QHeaderView
from controllers import AddProductDialog
from controllers import DeleteProductDialog
from controllers import SearchProductDialog

class ProductTableWidget(QTableWidget):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.current_page = 0
        self.records_per_page = 10
        self.update_table()

    def update_table(self):
        products = self.model.get_products()
        start = self.current_page * self.records_per_page
        end = start + self.records_per_page
        page_products = products[start:end]

        self.setRowCount(len(page_products))
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(["Название", "Производитель", "УНП", "Количество", "Адрес склада"])

        for row, product in enumerate(page_products):
            self.setItem(row, 0, QTableWidgetItem(product.name))
            self.setItem(row, 1, QTableWidgetItem(product.manufacturer_name))
            self.setItem(row, 2, QTableWidgetItem(product.unp))
            quantity_text = "Товара нет на складе" if product.quantity == 0 else str(product.quantity)
            self.setItem(row, 3, QTableWidgetItem(quantity_text))
            self.setItem(row, 4, QTableWidgetItem(product.warehouse_address))

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
    def change_records_per_page(self, records_per_page):
        self.records_per_page = records_per_page
        self.update_table()



class MainWindow(QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.setWindowTitle("Управление продуктами")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        # Добавляем кнопки загрузки и сохранения файла
        self.load_button = QPushButton("Загрузить")
        self.load_button.clicked.connect(self.load_from_file)
        layout.addWidget(self.load_button)

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_to_file)
        layout.addWidget(self.save_button)

        # Создаем экземпляр ProductTableWidget
        self.product_table = ProductTableWidget(self.model, parent=self)
        layout.addWidget(self.product_table)

        # Добавляем кнопки для добавления, удаления и поиска продуктов
        self.add_button = QPushButton("Добавить продукт")
        self.add_button.clicked.connect(self.open_add_product_dialog)
        layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Удалить продукт")
        self.delete_button.clicked.connect(self.open_delete_product_dialog)
        layout.addWidget(self.delete_button)

        self.search_button = QPushButton("Найти продукт")
        self.search_button.clicked.connect(self.open_search_product_dialog)
        layout.addWidget(self.search_button)

        # Добавляем элементы управления для навигации по страницам
        self.records_per_page_label = QLabel("Записей на странице:")
        layout.addWidget(self.records_per_page_label)

        self.records_per_page_combo = QComboBox()
        self.records_per_page_combo.addItems(["10", "20", "50", "100"])
        self.records_per_page_combo.currentTextChanged.connect(self.change_records_per_page)
        layout.addWidget(self.records_per_page_combo)

        self.central_widget.setLayout(layout)


        # Добавляем метку для отображения текущей страницы
        self.current_page_label = QLabel("Страница: 1")
        layout.addWidget(self.current_page_label)

        # Добавляем кнопки для навигации по страницам
        navigation_layout = QHBoxLayout()
        self.previous_page_button = QPushButton("Предыдущая страница")
        self.previous_page_button.clicked.connect(self.previous_page)
        navigation_layout.addWidget(self.previous_page_button)

        self.next_page_button = QPushButton("Следующая страница")
        self.next_page_button.clicked.connect(self.next_page)
        navigation_layout.addWidget(self.next_page_button)

        layout.addLayout(navigation_layout)

    def change_records_per_page(self, records_per_page_text):
            records_per_page = int(records_per_page_text)
            self.product_table.change_records_per_page(records_per_page)

    def load_from_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Загрузить файл", "", "XML файлы (*.xml)")
        if file_path:
            self.model.load_from_xml(file_path)
            self.product_table.update_table()

    def save_to_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "XML файлы (*.xml)")
        if file_path:
            self.model.save_to_xml(file_path)

    def open_add_product_dialog(self):
        dialog = AddProductDialog(self.model)
        if dialog.exec_() == QDialog.Accepted:
            self.product_table.update_table()

    def open_delete_product_dialog(self):
        dialog = DeleteProductDialog(self.model)
        if dialog.exec_() == QDialog.Accepted:
            self.product_table.update_table()

    def open_search_product_dialog(self):
        dialog = SearchProductDialog(self.model)
        dialog.exec_()

    def next_page(self):
        total_records = len(self.model.get_products())
        total_pages = (total_records + self.product_table.records_per_page - 1) // self.product_table.records_per_page
        if self.product_table.current_page < total_pages - 1:
            self.product_table.current_page += 1
            self.update_current_page_label()
            self.product_table.update_table()

    def previous_page(self):
        if self.product_table.current_page > 0:
            self.product_table.current_page -= 1
            self.update_current_page_label()
            self.product_table.update_table()

    def update_current_page_label(self):
        self.current_page_label.setText(f"Страница: {self.product_table.current_page + 1}")

