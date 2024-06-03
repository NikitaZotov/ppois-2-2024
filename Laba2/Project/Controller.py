# app/controller.py
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from Model import Record, RecordsHandler
from View import View
import xml.dom.minidom as minidom
import xml.sax

class Controller:
    def __init__(self):
        self.view = View(self)
        self.view.controller = self
        self.records = []
        self.current_page = 1
        self.faculty_combobox = None
        self.faculties = ["ФИТУ", "ФКП", "ФКСиС", "ФРЭ", "ИЭФ", "ФИБ", "ВФ"]
        self.departments_by_faculty = {
            "ФИТУ": ["ИИТ", "ИТАС", "ГД", "СУ", "ТОЭ", "ВМП"],
            "ФКП": ["ИКГ", "ИПЭ", "ИнЯз", "ПИКС", "ЭТИТ"],
            "ФКСиС": ["ПОИТ", "ЭВС", "ЭВМ", "Информатика", "ВМ", "Физика", "Философия"],
            "ФРЭ": ["Электроника", "ИР", "Микро- и наноэлектроника"],
            "ИЭФ": ["Менеджмент", "Экономика", "МПК", "ЭИ"],
            "ФИБ": ["ЗИ", "ИнфоКоммТехн", "ИнфИзмерСис", "Физвоспитание"],
            "ВФ": ["Связи", "РЭТ ВВС и войск ПВО", "Тактической и общевоенной подготовки"]
        }
        self.departments = set()
        self.ranks = ["Доцент", "Старший преподаватель", "Профессор", "Ассистент", "Заведующий кафедрой"]
        self.degrees = ["Кандидат наук", "Доктор наук", "Ничего"]

        # Initialize search fields as instance variables
        self.surname_entry = None
        self.department_entry = None
        self.rank_combobox = None
        self.faculty_combobox = None
        self.experience_from_entry = None
        self.experience_to_entry = None

    def save_records_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        if not file_path:
            return

        impl = minidom.getDOMImplementation()
        doc = impl.createDocument(None, "records", None)
        root = doc.documentElement

        for record in self.records:
            record_element = doc.createElement("record")

            faculty_element = doc.createElement("faculty")
            faculty_text = doc.createTextNode(record.faculty)
            faculty_element.appendChild(faculty_text)
            record_element.appendChild(faculty_element)

            department_element = doc.createElement("department")
            department_text = doc.createTextNode(record.department)
            department_element.appendChild(department_text)
            record_element.appendChild(department_element)

            professor_element = doc.createElement("professor")
            professor_text = doc.createTextNode(record.professor)
            professor_element.appendChild(professor_text)
            record_element.appendChild(professor_element)

            rank_element = doc.createElement("rank")
            rank_text = doc.createTextNode(record.rank)
            rank_element.appendChild(rank_text)
            record_element.appendChild(rank_element)

            degree_element = doc.createElement("degree")
            degree_text = doc.createTextNode(record.degree)
            degree_element.appendChild(degree_text)
            record_element.appendChild(degree_element)

            experience_element = doc.createElement("experience")
            experience_text = doc.createTextNode(str(record.experience))
            experience_element.appendChild(experience_text)
            record_element.appendChild(experience_element)

            root.appendChild(record_element)

        with open(file_path, "w", encoding="utf-8") as xml_file:
            doc.writexml(xml_file, addindent="  ", newl="\n", encoding="utf-8")

        messagebox.showinfo("Сохранение", "Файл успешно сохранен.")

    def load_records_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if not file_path:
            return

        handler = RecordsHandler()
        try:
            xml.sax.parse(file_path, handler)
            new_records = handler.records

            # Проверка на наличие дубликатов
            existing_records = {record: True for record in self.records}
            duplicate_records = [record for record in new_records if record in existing_records]

            if duplicate_records:
                message = "Найдены дубликаты записей. Хотите заменить существующие записи или добавить новые?"
                self.show_replace_or_add_dialog(
                    lambda choice: self.handle_duplicate_records(choice, new_records, duplicate_records))
            else:
                # Нет дубликатов, добавляем или заменяем записи напрямую
                def on_selection(choice):
                    if choice == "Заменить":
                        self.records = new_records
                    elif choice == "Добавить":
                        self.records.extend(new_records)
                    self.current_page = 1
                    self.update_view()
                    messagebox.showinfo("Загрузка", "Файл успешно загружен.")

                self.show_replace_or_add_dialog(on_selection)
        except Exception as e:
            messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить файл: {str(e)}")

    def handle_duplicate_records(self, choice, new_records, duplicate_records):
        """Обработка дубликатов записей."""
        if choice == "Заменить":
            for duplicate_record in duplicate_records:
                self.records.remove(duplicate_record)
            self.records.extend(new_records)
        elif choice == "Добавить":
            self.records.extend([record for record in new_records if record not in duplicate_records])
        self.current_page = 1
        self.update_view()
        messagebox.showinfo("Загрузка", "Файл успешно загружен.")

    def handle_duplicate_records(self, choice, new_records, duplicate_records):
        """Обработка дубликатов записей."""
        if choice == "Заменить":
            for duplicate_record in duplicate_records:
                self.records.remove(duplicate_record)
            self.records.extend(new_records)
        elif choice == "Добавить":
            self.records.extend([record for record in new_records if record not in duplicate_records])
        self.current_page = 1
        self.update_view()
        messagebox.showinfo("Загрузка", "Файл успешно загружен.")

    def show_replace_or_add_dialog(self, callback):
        dialog = tk.Toplevel(self.view)
        dialog.title("Загрузить записи")

        label = ttk.Label(dialog, text="Вы хотите заменить текущие записи или добавить к ним?")
        label.pack(padx=20, pady=10)

        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        replace_button = ttk.Button(button_frame, text="Заменить",
                                    command=lambda: [callback("Заменить"), dialog.destroy()])
        replace_button.pack(side=tk.LEFT, padx=10)

        add_button = ttk.Button(button_frame, text="Добавить", command=lambda: [callback("Добавить"), dialog.destroy()])
        add_button.pack(side=tk.LEFT, padx=10)

    def show_add_dialog(self):
        dialog = tk.Toplevel()
        dialog.title("Добавить запись")
        dialog.geometry("400x300")

        faculty_label = ttk.Label(dialog, text="Факультет:")
        faculty_label.pack()
        faculty_combobox = ttk.Combobox(dialog, values=self.faculties)
        faculty_combobox.pack()
        faculty_combobox.bind("<<ComboboxSelected>>", lambda event: self.update_departments_combobox(department_combobox, faculty_combobox.get()))

        department_label = ttk.Label(dialog, text="Название кафедры:")
        department_label.pack()
        department_combobox = ttk.Combobox(dialog, values=self.departments_by_faculty.get(faculty_combobox.get(), []))
        department_combobox.pack()

        professor_label = ttk.Label(dialog, text="ФИО преподавателя:")
        professor_label.pack()
        professor_entry = ttk.Entry(dialog)
        professor_entry.pack()

        rank_label = ttk.Label(dialog, text="Ученое звание:")
        rank_label.pack()
        rank_combobox = ttk.Combobox(dialog, values=self.ranks)
        rank_combobox.pack()

        degree_label = ttk.Label(dialog, text="Ученая степень:")
        degree_label.pack()
        degree_combobox = ttk.Combobox(dialog, values=self.degrees)
        degree_combobox.pack()

        experience_label = ttk.Label(dialog, text="Стаж работы:")
        experience_label.pack()
        experience_entry = ttk.Entry(dialog)
        experience_entry.pack()

        def validate_input(input_string):
            return bool(re.match(r"^[А-Яа-я\s]+$", input_string))


        def add_record():
            faculty = faculty_combobox.get()
            department = department_combobox.get()
            professor = professor_entry.get()
            rank = rank_combobox.get()
            degree = degree_combobox.get()
            experience = experience_entry.get()

            if not all([faculty, department, professor, rank, degree, experience]):
                messagebox.showwarning("Предупреждение", "Пожалуйста, заполните все поля.")
                return

            if not all(map(validate_input, [faculty, department, professor, rank, degree])):
                messagebox.showwarning("Предупреждение", "Поля факультет, кафедра, ФИО преподавателя, ученое звание и ученая степень должны содержать только русский алфавит.")
                return

            try:
                experience = int(experience)
            except ValueError:
                messagebox.showwarning("Предупреждение", "Стаж работы должен быть числом.")
                return

            # Создаем новую запись
            new_record = Record(faculty, department, professor, rank, degree, experience)

            # Проверяем наличие записи с такими же данными
            existing_record_index = None
            for index, record in enumerate(self.records):
                if record.equals(new_record):
                    existing_record_index = index
                    break

            if existing_record_index is not None:
                # Заменяем существующую запись новой
                self.records[existing_record_index] = new_record
                messagebox.showinfo("Добавление", "Запись успешно обновлена.")
            else:
                self.records.append(new_record)
                messagebox.showinfo("Добавление", "Запись успешно добавлена.")

            self.update_view()
            dialog.destroy()

        add_button = ttk.Button(dialog, text="Добавить", command=add_record)
        add_button.pack()

        cancel_button = ttk.Button(dialog, text="Отмена", command=dialog.destroy)
        cancel_button.pack()

    def show_delete_dialog(self):
        def delete_search_results():
            search_criteria = search_criteria_var.get()
            if search_criteria == "Фамилия преподавателя":
                search_text = self.surname_entry.get()
                search_results = self.search_records_by_surname(search_text)
            elif search_criteria == "Наименование кафедры":
                search_text = self.department_entry.get()
                search_results = self.search_records_by_department(search_text)
            elif search_criteria == "Ученое звание и факультет":
                search_rank = self.rank_combobox.get()
                search_faculty = self.faculty_combobox.get()
                search_results = self.search_records_by_rank_and_faculty(search_rank, search_faculty)
            elif search_criteria == "Стаж работы":
                experience_from = self.experience_from_entry.get()
                experience_to = self.experience_to_entry.get()
                search_results = self.search_records_by_experience(experience_from, experience_to)

            if not search_results:
                messagebox.showinfo("Поиск", "Нет записей для удаления по заданным критериям.")
            else:
                result = messagebox.askyesno("Удаление",
                                             f"Вы действительно хотите удалить {len(search_results)} записей?")
                if result:
                    for record in search_results:
                        self.records.remove(record)
                    self.update_view()
                    messagebox.showinfo("Удаление", f"Удалено записей: {len(search_results)}")

        delete_dialog = tk.Toplevel(self.view)
        delete_dialog.title("Выберите критерий поиска для удаления")

        ttk.Label(delete_dialog, text="Выберите критерий поиска:").grid(row=0, column=0)
        search_criteria_var = tk.StringVar()
        search_criteria_combobox = ttk.Combobox(delete_dialog, textvariable=search_criteria_var,
                                                values=["Фамилия преподавателя", "Наименование кафедры",
                                                        "Ученое звание и факультет", "Стаж работы"])
        search_criteria_combobox.grid(row=0, column=1)

        criteria_frame = ttk.Frame(delete_dialog)
        criteria_frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

        def update_search_fields(*args):
            for widget in criteria_frame.winfo_children():
                widget.destroy()

            if search_criteria_var.get() == "Фамилия преподавателя":
                ttk.Label(criteria_frame, text="Фамилия преподавателя:").grid(row=0, column=0)
                self.surname_entry = ttk.Entry(criteria_frame)
                self.surname_entry.grid(row=0, column=1)

            elif search_criteria_var.get() == "Наименование кафедры":
                ttk.Label(criteria_frame, text="Наименование кафедры:").grid(row=0, column=0)
                self.department_entry = ttk.Entry(criteria_frame)
                self.department_entry.grid(row=0, column=1)

            elif search_criteria_var.get() == "Ученое звание и факультет":
                ttk.Label(criteria_frame, text="Ученое звание:").grid(row=0, column=0)
                self.rank_combobox = ttk.Combobox(criteria_frame, values=sorted(self.ranks))
                self.rank_combobox.grid(row=0, column=1)

                ttk.Label(criteria_frame, text="Факультет:").grid(row=1, column=0)
                self.faculty_combobox = ttk.Combobox(criteria_frame, values=sorted(self.faculties))
                self.faculty_combobox.grid(row=1, column=1)

            elif search_criteria_var.get() == "Стаж работы":
                ttk.Label(criteria_frame, text="Стаж работы от:").grid(row=0, column=0)
                self.experience_from_entry = ttk.Entry(criteria_frame)
                self.experience_from_entry.grid(row=0, column=1)

                ttk.Label(criteria_frame, text="Стаж работы до:").grid(row=1, column=0)
                self.experience_to_entry = ttk.Entry(criteria_frame)
                self.experience_to_entry.grid(row=1, column=1)

        search_criteria_var.trace('w', update_search_fields)

        ttk.Button(delete_dialog, text="Удалить найденные записи", command=delete_search_results).grid(row=2, column=0,
                                                                                                       columnspan=2)

        delete_dialog.mainloop()

    def show_search_dialog(self):
        search_dialog = tk.Toplevel(self.view)
        search_dialog.title("Search Faculty Records")

        ttk.Label(search_dialog, text="Критерий поиска:").grid(row=0, column=0)
        search_criteria_var = tk.StringVar()
        search_criteria_combobox = ttk.Combobox(search_dialog, textvariable=search_criteria_var, values=["Фамилия преподавателя","Наименование кафедры", "Ученое звание и факультет", "Стаж работы"])
        search_criteria_combobox.grid(row=0, column=1)

        criteria_frame = ttk.Frame(search_dialog)
        criteria_frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

        # Function to update search fields based on criteria
        def update_search_fields(*args):
            for widget in criteria_frame.winfo_children():
                widget.destroy()

            # Reset instance variables
            self.surname_entry = None
            self.department_entry = None
            self.rank_combobox = None
            self.faculty_combobox = None
            self.experience_from_entry = None
            self.experience_to_entry = None

            if search_criteria_var.get() == "Фамилия преподавателя" :
                ttk.Label(criteria_frame, text="ФИО преподавателя:").grid(row=0, column=0)
                self.surname_entry = ttk.Entry(criteria_frame)
                self.surname_entry.grid(row=0, column=1)

            elif search_criteria_var.get() == "Наименование кафедры":
                ttk.Label(criteria_frame, text="Название кафедры:").grid(row=0, column=0)
                self.department_entry = ttk.Entry(criteria_frame)
                self.department_entry.grid(row=1, column=1)

            elif search_criteria_var.get() == "Ученое звание и факультет":
                ttk.Label(criteria_frame, text="Ученое звание:").grid(row=0, column=0)
                rank_var = tk.StringVar()
                self.rank_combobox = ttk.Combobox(criteria_frame, textvariable=rank_var, values=sorted(self.ranks))
                self.rank_combobox.grid(row=0, column=1)

                ttk.Label(criteria_frame, text="Факультет:").grid(row=1, column=0)
                faculty_var = tk.StringVar()
                self.faculty_combobox = ttk.Combobox(criteria_frame, textvariable=faculty_var, values=sorted(self.faculties))
                self.faculty_combobox.grid(row=1, column=1)

            elif search_criteria_var.get() == "Стаж работы":
                ttk.Label(criteria_frame, text="Стаж работы от:").grid(row=0, column=0)
                self.experience_from_entry = ttk.Entry(criteria_frame)
                self.experience_from_entry.grid(row=0, column=1)

                ttk.Label(criteria_frame, text="Стаж работы до:").grid(row=1, column=0)
                self.experience_to_entry = ttk.Entry(criteria_frame)
                self.experience_to_entry.grid(row=1, column=1)

        search_criteria_var.trace('w', update_search_fields)

        def perform_search():
            criteria = search_criteria_var.get()
            search_results = []
            if criteria == "Фамилия преподавателя" :
                surname = self.surname_entry.get() if self.surname_entry else ""
                search_results = self.search_records_by_surname(surname)

            elif criteria == "Наименование кафедры":
                department = self.department_entry.get() if self.department_entry else ""
                search_results = self.search_records_by_department(department)
            elif criteria == "Ученое звание и факультет":
                rank = self.rank_combobox.get() if self.rank_combobox else ""
                faculty = self.faculty_combobox.get() if self.faculty_combobox else ""
                search_results = self.search_records_by_rank_and_faculty(rank, faculty)
            elif criteria == "Стаж работы":
                experience_from = self.experience_from_entry.get() if self.experience_from_entry else ""
                experience_to = self.experience_to_entry.get() if self.experience_to_entry else ""
                search_results = self.search_records_by_experience(experience_from, experience_to)
            self.view.update_search_results_tree(search_results, search_results_tree)

            if not search_results:
                messagebox.showinfo("Поиск", "Записи не найдены.")
            else:
                messagebox.showinfo("Поиск", f"Найдено записей: {len(search_results)}")

        ttk.Button(search_dialog, text="Поиск", command=perform_search).grid(row=2, column=0, columnspan=2)

        search_results_tree = ttk.Treeview(search_dialog, columns=("Факультет", "Название кафедры", "ФИО преподавателя", "Ученое звание", "Ученая степень", "Стаж работы"))
        search_results_tree.heading("#0", text="ID")
        search_results_tree.heading("Факультет", text="Факультет")
        search_results_tree.heading("Название кафедры", text="Название кафедры")
        search_results_tree.heading("ФИО преподавателя", text="ФИО преподавателя")
        search_results_tree.heading("Ученое звание", text="Ученое звание")
        search_results_tree.heading("Ученая степень", text="Ученая степень")
        search_results_tree.heading("Стаж работы", text="Стаж работы")
        search_results_tree.grid(row=3, column=0, columnspan=2, sticky='nsew')

        search_dialog.grid_rowconfigure(3, weight=1)
        search_dialog.grid_columnconfigure(1, weight=1)

    def search_records_by_surname(self, surname):
        search_results = []
        for record in self.records:
            if surname and surname in record.professor:
                search_results.append(record)
        return search_results

    def search_records_by_department(self, department):
        search_results = []
        for record in self.records:
            if department and department in record.department:
                search_results.append(record)
        return search_results
    def search_records_by_rank_and_faculty(self, rank, faculty):
        search_results = []
        for record in self.records:
            if rank and rank == record.rank and faculty and faculty == record.faculty:
                search_results.append(record)
        return search_results

    def search_records_by_experience(self, experience_from, experience_to):
        search_results = []
        try:
            experience_from = int(experience_from)
            experience_to = int(experience_to)
        except ValueError:
            return search_results

        for record in self.records:
            try:
                experience = int(record.experience)
                if experience_from <= experience <= experience_to:
                    search_results.append(record)
            except ValueError:
                continue
        return search_results

    def update_view(self):
        total_records = len(self.records)
        total_pages = (total_records + self.view.records_per_page - 1) // self.view.records_per_page

        start = (self.current_page - 1) * self.view.records_per_page
        end = start + self.view.records_per_page
        current_records = self.records[start:end]

        self.view.update_records_list(current_records)
        self.view.update_page_info(total_pages, self.current_page)
        self.view.update_records_info()
    def update_departments_combobox(self, department_combobox, faculty):
        departments = self.departments_by_faculty.get(faculty, [])
        department_combobox["values"] = departments

    def first_page(self):
        self.current_page = 1
        self.update_view()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_view()

    def next_page(self):
        total_records = len(self.records)
        total_pages = (total_records + self.view.records_per_page - 1) // self.view.records_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.update_view()

    def last_page(self):
        total_records = len(self.records)
        total_pages = (total_records + self.view.records_per_page - 1) // self.view.records_per_page
        self.current_page = total_pages
        self.update_view()