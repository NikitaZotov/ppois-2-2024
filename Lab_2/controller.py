import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
class ClientController:
    def __init__(self,view, model):
        self.model = model
        self.view = view
        self.view.set_controller(self)
        self.view.create_widgets()
        self.view.create_pagination_controls()
        self.view.update_view()

    def add_client_to_model(self, client_info):
        # Код для добавления информации о новом клиенте
        self.model.add_client(client_info)
        self.view.set_controller(self)
        self.view.update_view()

    def get_clients(self):
        # Возвращает список всех клиентов из модели
        return self.model.get_page_data()

    def save_clients_to_xml(self):
        filepath = tk.filedialog.asksaveasfilename(defaultextension=".xml",
                                                   filetypes=[("XML files", "*.xml")])
        if filepath:  # Проверка, что пользователь выбрал путь для сохранения файла
            self.model.save_to_xml_dom(filepath)

    def load_from_file(self):
        # Диалог выбора файла
        filepath = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if not filepath:  # Пользователь закрыл окно выбора файла или не выбрал файл
            return
        self.model.load_clients_from_xml(filepath)
        self.view.update_view()

    def find_client(self, search_query):
        return self.model.search_clients(**search_query)

    def delete_client(self, query):
        if self.model.delete_client(query):
            self.view.show_message('Успех', 'Клиент удален.')
        else:
            self.view.show_message('Ошибка', 'Клиент не найден.')
        self.view.set_controller(self)
        self.view.update_view()

    def get_page_items(self):
        return self.model.get_page_items()

    def set_items_per_page(self, items_per_page):
        self.model.set_items_per_page(items_per_page)
        self.view.update_view()

    def change_page(self, new_page):
        self.model.current_page = new_page
        self.view.update_view()

    def next_page(self):
        self.model.go_to_next_page()
        self.view.update_view()

    def previous_page(self):
        self.model.go_to_previous_page()
        self.view.update_view()

    def first_page(self):
        self.model.go_to_first_page()
        self.view.update_view()

    def last_page(self):
        self.model.go_to_last_page()
        self.view.update_view()

    def get_current_page_data(self):
        return self.model.get_page_data()

    def get_records_per_page(self):
        return self.model.clients_per_page

    def get_total_records(self):
        return len(self.model.clients_list)

    def get_current_page(self):
        return self.model.current_page

    def get_total_pages(self):
        return -(len(self.model.clients_list) // -self.model.clients_per_page)

    def set_items_per_page(self, items_per_page):
        self.model.set_items_per_page(items_per_page)
        self.model.go_to_first_page()
        self.view.update_view()
        if self.view.combobox_records_per_page.get() == str(items_per_page):
            self.model.paginator.go_to_last_page()
            self.view.update_view()

    def last_page(self):
        self.model.go_to_last_page()
        self.view.update_view()
