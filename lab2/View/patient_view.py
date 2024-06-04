import tkinter as tk
from tkinter import ttk, messagebox
from Models.patient import Patient

class PatientView():
    def __init__(self, window, controller, table_view):
        self.controller = controller
        self.table_view = table_view
        self.labels = ["ФИО пациента", "Адрес прописки", "Дата рождения", "Дата приема", "ФИО врача", "Заключение"]
        self.entries = []

        for i, label_text in enumerate(self.labels):
            label = tk.Label(window, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=5)

            entry = tk.Entry(window)
            if label_text in ["Дата рождения", "Дата приема"]:
                entry.insert(tk.END, "DD.MM.YYYY")
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
        if not all(values):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return
        if not values[2].startswith("DD.MM.YYYY") or not values[3].startswith("DD.MM.YYYY"):
            messagebox.showerror("Ошибка", "Формат даты должен быть DD.MM.YYYY.")
            return
        new_patient = Patient(*values)
        self.controller.add_patient(new_patient)
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

        selected_search_type = tk.StringVar()
        delete_type_combobox = ttk.Combobox(delete_dialog,
                                            values=["ФИО пациента или адресу прописки", "Дата рождения",
                                                    "ФИО врача или дате приема"],
                                            textvariable=selected_search_type)
        delete_type_combobox.pack(pady=5)

        delete_entry = tk.Entry(delete_dialog)
        delete_entry.pack(padx=10, pady=5)

        delete_button = tk.Button(delete_dialog, text="Удалить",
                                  command=lambda: self.perform_delete(selected_search_type.get(), delete_entry.get()))
        delete_button.pack(pady=10)

    def perform_delete(self, delete_type, query):
        if not delete_type or not query:
            messagebox.showerror("Ошибка", "Оба поля (тип и запрос) должны быть заполнены.")
            return
        if delete_type not in ["ФИО пациента или адресу прописки", "Дата рождения", "ФИО врача или дате приема"]:
            messagebox.showerror("Ошибка", "Неверный тип удаления.")
            return
        self.controller.delete_patient(delete_type, query)
        self.table_view.update_table()


    def open_search_dialog(self):
        search_dialog = tk.Toplevel()
        search_dialog.title("Поиск")

        search_type_label = tk.Label(search_dialog, text="Тип поиска:")
        search_type_label.pack(padx=10, pady=5)

        selected_search_type = tk.StringVar()
        search_type_combobox = ttk.Combobox(search_dialog,
                                            values=["ФИО пациента или адресу прописки", "Дата рождения",
                                                    "ФИО врача или дате приема"],
                                            textvariable=selected_search_type)
        search_type_combobox.pack(pady=5)

        search_entry = tk.Entry(search_dialog)
        search_entry.pack(padx=10, pady=5)

        search_button = tk.Button(search_dialog, text="Искать",
                                  command=lambda: self.perform_search(selected_search_type.get(), search_entry.get(),
                                                                      search_results_tree))
        search_button.pack(pady=10)

        # Create Treeview for search results
        columns = ("full_name", "address", "birth_date", "appointment_date", "doctor_name", "conclusion")
        column_names = ["ФИО пациента", "Адрес прописки", "Дата рождения", "Дата приема", "ФИО врача", "Заключение"]
        search_results_tree = ttk.Treeview(search_dialog, columns=columns, show='headings')

        for col, col_name in zip(columns, column_names):
            search_results_tree.heading(col, text=col_name)
            search_results_tree.column(col, minwidth=0, width=100, stretch=tk.NO)

        search_results_tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def perform_search(self, search_type, query, treeview):
        if not search_type or not query:
            messagebox.showerror("Ошибка", "Оба поля (тип и запрос) должны быть заполнены.")
            return
        if search_type not in ["ФИО пациента или адресу прописки", "Дата рождения", "ФИО врача или дате приема"]:
            messagebox.showerror("Ошибка", "Неверный тип поиска.")
            return
        results = self.controller.search_patient(search_type, query)

        # Clear existing results
        for row in treeview.get_children():
            treeview.delete(row)

        # Insert new results
        for patient in results:
            treeview.insert("", tk.END, values=(
            patient.full_name, patient.address, patient.birth_date, patient.appointment_date, patient.doctor_name,
            patient.conclusion))
