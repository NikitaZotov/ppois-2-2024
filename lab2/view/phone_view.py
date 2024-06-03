import tkinter as tk
from tkinter import ttk
from models.phone import Phone
from view.phone_table_view import PhoneTableView


class PhoneView:
    def __init__(self, window, controller, table_view):
        self.controller = controller
        self.table_view = table_view

        self.labels = ["ФИО клиента", "Номер счета", "Адрес прописки", "Мобильный телефон", "Городской телефон"]
        self.entries = []

        for i, label_text in enumerate(self.labels):
            label = tk.Label(window, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=5)

            entry = tk.Entry(window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries.append(entry)

        self.add_button = tk.Button(window, text="Добавить", command=self.add_to_table)
        self.add_button.grid(row=len(self.labels), column=0, columnspan=2, pady=10)

        self.search_button = tk.Button(window, text="Поиск", command=self.open_search_dialog)
        self.search_button.grid(row=len(self.labels), column=1, pady=10)

        self.delete_button = tk.Button(window, text="Удалить", command=self.open_delete_dialog)
        self.delete_button.grid(row=len(self.labels) + 1, column=0, columnspan=2, pady=10)

    def add_to_table(self):
        values = [entry.get() for entry in self.entries]
        if all(values):
            new_phone = Phone(*values)
            self.controller.add_phone(new_phone)
            self.clear_entries()
            self.table_view.update_table()

    def clear_entries(self):
        for entry in self.entries:
            entry.delete(0, tk.END)

    def open_delete_dialog(self):
        delete_dialog = tk.Toplevel()
        delete_dialog.title("Удаление")

        delete_type_label = tk.Label(delete_dialog, text="Тип удаления:")
        delete_type_label.pack(padx=10, pady=5)

        delete_type_combobox = ttk.Combobox(delete_dialog, values=[
            "ФИО клиента или номер телефона",
            "Номер счета или адрес",
            "ФИО клиента и цифры в номере"
        ])
        delete_type_combobox.pack(padx=10, pady=5)

        query_label = tk.Label(delete_dialog, text="Запрос:")
        query_label.pack(padx=10, pady=5)

        query_entry = tk.Entry(delete_dialog)
        query_entry.pack(padx=10, pady=5)

        def delete_phone():
            delete_type = delete_type_combobox.get()
            query = query_entry.get()
            self.controller.delete_phone(delete_type, query)
            self.table_view.update_table()
            delete_dialog.destroy()

        delete_button = tk.Button(delete_dialog, text="Удалить", command=delete_phone)
        delete_button.pack(padx=10, pady=10)

    def open_search_dialog(self):
        search_dialog = tk.Toplevel()
        search_dialog.title("Поиск")

        search_type_label = tk.Label(search_dialog, text="Тип поиска:")
        search_type_label.pack(padx=10, pady=5)

        search_type_combobox = ttk.Combobox(search_dialog, values=[
            "ФИО клиента или номер телефона",
            "Номер счета или адрес",
            "ФИО клиента и цифры в номере"
        ])
        search_type_combobox.pack(padx=10, pady=5)

        query_label = tk.Label(search_dialog, text="Запрос:")
        query_label.pack(padx=10, pady=5)

        query_entry = tk.Entry(search_dialog)
        query_entry.pack(padx=10, pady=5)

        search_result_table = ttk.Treeview(search_dialog, columns=self.labels, show='headings')
        for label in self.labels:
            search_result_table.heading(label, text=label)
        search_result_table.pack(padx=10, pady=10)

        def search_phone():
            search_type = search_type_combobox.get()
            query = query_entry.get()
            results = self.controller.search_phone(search_type, query)
            for row in search_result_table.get_children():
                search_result_table.delete(row)
            for phone in results:
                search_result_table.insert('', 'end', values=[
                    phone.full_name,
                    phone.account_number,
                    phone.address,
                    phone.mobile,
                    phone.landline
                ])

        search_button = tk.Button(search_dialog, text="Поиск", command=search_phone)
        search_button.pack(padx=10, pady=10)
