from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, QMessageBox
)
from model import Product

class AddProductDialog(QDialog):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.setWindowTitle("Добавить продукт")

        layout = QVBoxLayout()

        self.name_edit = QLineEdit()
        self.manufacturer_name_edit = QLineEdit()
        self.unp_edit = QLineEdit()
        self.quantity_edit = QLineEdit()
        self.warehouse_address_edit = QLineEdit()

        layout.addWidget(QLabel("Название"))
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel("Название производителя"))
        layout.addWidget(self.manufacturer_name_edit)
        layout.addWidget(QLabel("УНП"))
        layout.addWidget(self.unp_edit)
        layout.addWidget(QLabel("Количество"))
        layout.addWidget(self.quantity_edit)
        layout.addWidget(QLabel("Адрес склада"))
        layout.addWidget(self.warehouse_address_edit)

        add_button = QPushButton("Добавить")
        add_button.clicked.connect(self.add_product)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def add_product(self):
        name = self.name_edit.text().strip()
        manufacturer_name = self.manufacturer_name_edit.text().strip()
        unp = self.unp_edit.text().strip()
        warehouse_address = self.warehouse_address_edit.text().strip()

        try:
            quantity = int(self.quantity_edit.text())
            if quantity < 0:
                raise ValueError("Количество должно быть неотрицательным")
            elif len(unp) != 13:
                raise ValueError("УНП должен состоять из 13 цифр")
        except ValueError as e:
            QMessageBox.critical(self, "Ошибка", str(e))
            return

        product = Product(
            name=name,
            manufacturer_name=manufacturer_name,
            unp=unp,
            quantity=quantity,
            warehouse_address=warehouse_address
        )

        self.model.add_product(product)
        self.accept()

class SearchProductDialog(QDialog):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.setWindowTitle("Поиск продукта")

        layout = QVBoxLayout()

        self.search_type_combo = QComboBox()
        self.search_type_combo.addItem("Название или Количество")
        self.search_type_combo.addItem("Производитель или УНП")
        self.search_type_combo.addItem("Адрес хранения")
        layout.addWidget(QLabel("Тип поиска"))
        layout.addWidget(self.search_type_combo)

        self.search_value_edit = QLineEdit()
        layout.addWidget(QLabel("Введите значение"))
        layout.addWidget(self.search_value_edit)

        search_button = QPushButton("Поиск")
        search_button.clicked.connect(self.perform_search)
        layout.addWidget(search_button)

        self.setLayout(layout)

    def perform_search(self):
        search_type = self.search_type_combo.currentText()
        search_value = self.search_value_edit.text().strip()

        if not search_value:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, введите значение.")
            return

        if search_type == "Название или Количество" and search_value.isdigit() and int(search_value) == 0:
            QMessageBox.information(self, "Информация", "Товары с количеством 0 не найдены.")
            return

        if search_type == "Название или Количество":
            products = self.model.find_products_by_name_or_quantity(search_value)
        elif search_type == "Производитель или УНП":
            products = self.model.find_products_by_manufacturer_or_unp(search_value)
        else: 
            products = self.model.find_products_by_storage_address(search_value)

        if products:
            self.list_products(products)
        else:
            QMessageBox.information(self, "Информация", "Товары не найдены.")

    def list_products(self, products):
        layout = QVBoxLayout()
        for product in products:
            layout.addWidget(QLabel(f"{product.name} - {product.manufacturer_name} - {product.unp} - {product.quantity} - {product.warehouse_address}"))
        dialog = QDialog(self)
        dialog.setLayout(layout)
        dialog.exec_()

class DeleteProductDialog(QDialog):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.setWindowTitle("Удалить продукт")

        layout = QVBoxLayout()

        self.criteria_combo = QComboBox()
        self.criteria_combo.addItem("Название или Количество")
        self.criteria_combo.addItem("Производитель или УНП")
        self.criteria_combo.addItem("Адрес склада")

        self.value_edit = QLineEdit()

        layout.addWidget(QLabel("Критерий"))
        layout.addWidget(self.criteria_combo)
        layout.addWidget(QLabel("Значение"))
        layout.addWidget(self.value_edit)

        delete_button = QPushButton("Удалить")
        delete_button.clicked.connect(self.delete_product)
        layout.addWidget(delete_button)

        self.setLayout(layout)

    def delete_product(self):
        criteria = self.criteria_combo.currentText()
        value = self.value_edit.text().strip()
        if not value:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, введите значение.")
            return

        removed_products = []
        if criteria == "Название или Количество":
            if value.isdigit():
                removed_products = self.model.remove_product_by_criteria("quantity", value)
            else:
                removed_products = self.model.remove_product_by_criteria("name", value)
        elif criteria == "Производитель или УНП":
            if value.isdigit() and len(value) == 13:
                removed_products = self.model.remove_product_by_criteria("unp", value)
            else:
                removed_products = self.model.remove_product_by_criteria("manufacturer_name", value)
        elif criteria == "Адрес склада":
            removed_products = self.model.remove_product_by_criteria("warehouse_address", value)

        if removed_products:
            QMessageBox.information(self, "Результат удаления", f"Удалено {len(removed_products)} продуктов")
            self.accept()  
        else:
            QMessageBox.information(self, "Результат удаления", "Продукты по заданным критериям не найдены.")



