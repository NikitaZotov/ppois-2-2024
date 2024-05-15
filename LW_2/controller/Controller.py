import math

from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtWidgets
from view.AddPetDialog import AddPetDialog
from view.SearchByFilterDialog import SearchByFilterDialog
from view.DeleteByFilter import DeleteByFilter

class PetController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.btn_create_file.clicked.connect(self.save_to_xml)
        self.view.btn_open_file.clicked.connect(self.load_from_xml)
        self.view.btn_prev_page.clicked.connect(self.show_prev_page)
        self.view.btn_next_page.clicked.connect(self.show_next_page)
        self.view.btn_first_page.clicked.connect(self.go_to_first_page)
        self.view.btn_last_page.clicked.connect(self.go_to_last_page)
        self.view.spinBox.valueChanged.connect(self.update_page_size)
        self.view.btn_add_pet.clicked.connect(self.add_pet_dialog)
        self.view.btn_search_by_filter.clicked.connect(self.show_search_dialog)
        self.view.btn_return_to_initial.clicked.connect(self.return_to_initial_table)
        self.view.btn_delete_by_filter.clicked.connect(self.delete_by_filter_dialog)
        self.model.add_observer(self)

    def save_to_xml(self):
        # Call the model to save data to XML
        file_path, _ = QFileDialog.getSaveFileName(None, "Save File", "", "XML Files (*.xml)")
        if file_path:
            # Save data to XML
            self.model.save_to_xml(file_path)

    def load_from_xml(self):
        # Call the model to load data from XML
        file_path, _ = QFileDialog.getOpenFileName(None, "Open File", "", "XML Files (*.xml)")
        if file_path:
            self.model.load_from_xml(file_path)
            self.model_is_changed()


    def show_prev_page(self):
        if self.view.current_page > 1:
            self.view.current_page -= 1
            self.view.show_records(self.model.records)
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "Already at the first page.")

    def show_next_page(self):
        if self.view.current_page < self.view.total_pages:
            self.view.current_page += 1
            self.view.show_records(self.model.records)
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "Already at the last page.")

    def go_to_first_page(self):
        try:
            self.view.current_page = 1
            self.view.show_records(self.model.records)
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Warning", f"There are no records to display: {str(e)}")

    def go_to_last_page(self):
        try:
            self.view.current_page = self.view.total_pages
            self.view.show_records(self.model.records)
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Warning", f"There are no records to display: {str(e)}")

    def update_page_size(self, value):
        try:
            self.view.page_size = value
            self.view.total_pages = math.ceil(len(self.model.records) / self.view.page_size)
            self.view.show_records(self.model.records)
            self.view.current_page = min(self.view.current_page, self.view.total_pages)
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"There are no records to display: {str(e)}")

    def add_pet_dialog(self):
        if self.model.records:
            dialog = AddPetDialog()
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                pet_info = dialog.get_pet_info()
                if pet_info is not None:
                    self.model.add_pet(pet_info)
                    self.model_is_changed()
        else:
            QtWidgets.QMessageBox.information(self.view.centralwidget, "Add pet", "There are no records to delete.")

    def show_search_dialog(self):
        if self.model.records:
            dialog = SearchByFilterDialog()
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                search_criteria = dialog.get_search_criteria()
                self.view.show_records(self.model.perform_search(search_criteria))
                self.view.btn_return_to_initial.setVisible(True)
                self.view.spinBox.setEnabled(False)
        else:
            QtWidgets.QMessageBox.information(self.view.centralwidget, "Search", "There are no records to search.")

    def delete_by_filter_dialog(self):
        if self.model.records:
            dialog = DeleteByFilter()
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                search_criteria = dialog.get_search_criteria()
                self.model.delete_items(search_criteria)
                self.model_is_changed()
        else:
            QtWidgets.QMessageBox.information(self.view.centralwidget, "Delete", "There are no records to delete.")

    def return_to_initial_table(self):
        self.view.clear_table()
        self.view.show_records(self.model.records)
        self.view.btn_return_to_initial.setVisible(False)

    def model_is_changed(self):
        self.view.show_records(self.model.records)