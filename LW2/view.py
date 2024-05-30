from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning
from model import Model
from controller import Controller


class View:
    def __init__(self, model: Model, controller: Controller):
        self.page_label = None
        self.next_button = None
        self.records_per_page_label = None
        self.total_records_label = None
        self.prev_button = None
        self.first_page_button = None
        self.last_page_button = None
        self.items_per_page_var = None
        self.items_per_page_entry = None
        self.update_button = None
        self.reset_button = None
        self.file_menu = None
        self.table = None
        self.model = model
        self.controller = controller
        self.current_person = None
        self.controller.setView(self)
        self.root = Tk()
        self.root.title("Меню")
        self.root.geometry("1150x550")
        self.root.resizable(False, False)
        self.create_main_menu()
        self.create_table()
        self.create_pagination_buttons()
        self.update_table()

    def update_table(self):
        # Очищаем таблицу перед добавлением новых данных
        for item in self.table.get_children():
            self.table.delete(item)

        # Добавляем персоны текущей страницы из контроллера
        for person in self.controller.get_current_page_items():
            self.table.insert("", "end", values=person)

        # Обновляем кнопки пагинации и количество записей
        self.update_pagination_buttons()

    def create_table(self):
        columns = ("faculty", "department", "SNP", "academic_title", "academic_degree", "work_exp")
        self.table = ttk.Treeview(columns=columns, show="headings")
        self.table.pack(fill=BOTH, expand=1)
        self.table.heading("faculty", text="Факультет")
        self.table.heading("department", text="Кафедра")
        self.table.heading("SNP", text="ФИО")
        self.table.heading("academic_title", text="Ученое звание")
        self.table.heading("academic_degree", text="Ученая степень")
        self.table.heading("work_exp", text="Стаж работы")
        self.table.column("#1", width=100)
        self.table.column("#2", width=150)
        self.table.column("#6", width=100)

    def create_pagination_buttons(self):
        button_frame = ttk.Frame(self.root)
        button_frame.pack(side=BOTTOM, fill=X)

        center_frame = ttk.Frame(button_frame)
        center_frame.pack(side=TOP, expand=True)

        self.first_page_button = ttk.Button(center_frame, text="Первая страница", command=self.controller.first_page)
        self.first_page_button.pack(side=LEFT)

        self.prev_button = ttk.Button(center_frame, text="Предыдущая страница", command=self.controller.previous_page)
        self.prev_button.pack(side=LEFT)

        self.page_label = ttk.Label(center_frame, text=f"Страница {self.controller.current_page + 1}")
        self.page_label.pack(side=LEFT, padx=10)

        self.next_button = ttk.Button(center_frame, text="Следующая страница", command=self.controller.next_page)
        self.next_button.pack(side=LEFT)

        self.last_page_button = ttk.Button(center_frame, text="Последняя страница", command=self.controller.last_page)
        self.last_page_button.pack(side=LEFT)

        records_label_frame = ttk.Frame(center_frame)
        records_label_frame.pack(side=LEFT, padx=10)

        self.records_per_page_label = ttk.Label(records_label_frame,
                                                text=f"Записей на текущей странице: {self.controller.items_per_page}")
        self.records_per_page_label.pack(side=TOP)

        self.total_records_label = ttk.Label(records_label_frame,
                                             text=f"Всего записей: {len(self.model.get_current_persons())}")
        self.total_records_label.pack(side=TOP)

        items_per_page_frame = ttk.Frame(center_frame)
        items_per_page_frame.pack(side=LEFT, padx=10)

        ttk.Label(items_per_page_frame, text="Записей на страницу:").pack(side=LEFT)
        self.items_per_page_var = StringVar(value=self.controller.items_per_page)
        self.items_per_page_entry = ttk.Entry(items_per_page_frame, textvariable=self.items_per_page_var, width=5)
        self.items_per_page_entry.pack(side=LEFT)
        self.items_per_page_entry.bind("<Return>", self.update_items_per_page)

        self.update_button = ttk.Button(items_per_page_frame, text="Обновить", command=self.update_items_per_page)
        self.update_button.pack(side=LEFT)

    def update_items_per_page(self, event=None):
        try:
            items_per_page = int(self.items_per_page_var.get())
            if items_per_page > 0:
                self.controller.set_items_per_page(items_per_page)
                self.update_table()
            else:
                raise ValueError
        except ValueError:
            showerror("Ошибка", "Введите положительное целое число для количества записей на страницу")

    def update_pagination_buttons(self):
        self.prev_button.config(state=NORMAL if self.controller.has_previous_page() else DISABLED)
        self.next_button.config(state=NORMAL if self.controller.has_next_page() else DISABLED)
        self.first_page_button.config(state=NORMAL if self.controller.has_previous_page() else DISABLED)
        self.last_page_button.config(state=NORMAL if self.controller.has_next_page() else DISABLED)
        self.page_label.config(text=f"Страница {self.controller.current_page + 1}")
        self.records_per_page_label.config(
            text=f"Записей на текущей странице: {len(self.controller.get_current_page_items())}")
        self.total_records_label.config(text=f"Всего записей: {len(self.model.get_current_persons())}")

    def serialize(self):
        try:
            self.controller.serialize()
        except ValueError as e:
            showerror(title="Ошибка", message=str(e))

    def deserialize(self):
        try:
            self.controller.deserialize()
            self.update_table()
        except ValueError as e:
            showerror(title="Ошибка", message=str(e))

    def create_main_menu(self):
        main_menu = Menu(self.root)
        self.file_menu = Menu(main_menu, tearoff=0)
        self.file_menu.add_command(label="Сохранить", command=self.serialize)  # serialize
        self.file_menu.add_command(label="Открыть", command=self.deserialize)
        self.file_menu.add_command(label="Найти эл-нт", command=self.search)
        self.file_menu.add_command(label="Добавить эл-нт", command=self.add_element)
        self.file_menu.add_command(label="Удалить эл-нт", command=self.delete_element)
        self.file_menu.add_command(label="Сброс", command=self.reset_search, state=DISABLED)
        self.file_menu.add_separator()
        main_menu.add_cascade(label="Файл", menu=self.file_menu)
        self.root.config(menu=main_menu)

    def add_element(self):

        window = Tk()  # Создание нового окна
        window.title("Добавление")
        window.geometry("925x250")
        window.resizable(False, False)
        frame = ttk.Frame(window, borderwidth=1, relief=SOLID, padding=[10, 10])

        faculties = list(set([self.model.persons[i][0] for i in range(len(self.model.persons))]))
        department = list(set([self.model.persons[i][1] for i in range(len(self.model.persons))]))
        snp = list(set([self.model.persons[i][2] for i in range(len(self.model.persons))]))
        academic_title = list(set([self.model.persons[i][3] for i in range(len(self.model.persons))]))
        academic_degree = list(set([self.model.persons[i][4] for i in range(len(self.model.persons))]))
        work_exp = list(set([self.model.persons[i][5] for i in range(len(self.model.persons))]))
        # Создание и настройка комбо-боксов и меток
        comboboxes = [ttk.Combobox(frame) for _ in range(6)]  #
        labels = ["Факультет", "Название кафедры", "ФИО преподавателя", "Ученое звание", "Ученая степень",
                  "Стаж работы"]
        for i, label in enumerate(labels):
            ttk.Label(frame, text=label).grid(row=0, column=i)
            comboboxes[i].grid(row=1, column=i)
        comboboxes[0]['values'] = faculties
        comboboxes[1]['values'] = department
        comboboxes[2]['values'] = snp
        comboboxes[3]['values'] = academic_title
        comboboxes[4]['values'] = academic_degree
        comboboxes[5]['values'] = work_exp

        frame.grid(padx=20, pady=20, columnspan=10, sticky=EW)

        def on_add():
            try:
                person = tuple(combo.get() for combo in comboboxes)
                self.controller.add_to_model(person)
                self.update_table()  # Обновляем таблицу после добавления персоны
                window.destroy()
            except ValueError as e:
                window.destroy()
                showerror(title="Ошибка", message=str(e))

        # Создание кнопки "Добавить"
        btn_add = ttk.Button(window, text="Добавить", command=on_add)

        btn_add.place(relx=0.89, rely=0.85)

        window.mainloop()  # Запуск главного цикла событий для окна

    def show_error(self, message):
        showerror("Ошибка", message)

    def delete_element(self):
        def create_conditions(entries):
            conditions = []
            faculty, department, SNP, academic_title, academic_degree, work_exp_min, work_exp_max = entries

            if SNP.get():
                snp_parts = SNP.get().split()
                conditions.append(lambda person: any(part in person[2] for part in snp_parts))
            if department.get() and department.get() in departments:
                conditions.append(lambda person: person[1] == department.get())
            if academic_title.get() and academic_title.get() in academic_titles:
                conditions.append(lambda person: person[3] == academic_title.get())
            if academic_degree.get() and academic_degree.get() in academic_degrees:
                conditions.append(lambda person: person[4] == academic_degree.get())
            if faculty.get() and faculty.get() in faculties:
                conditions.append(lambda person: person[0] == faculty.get())
            if work_exp_min.get() and work_exp_max.get():
                try:
                    min_exp = int(work_exp_min.get())
                    max_exp = int(work_exp_max.get())
                    if min_exp > max_exp:
                        window.destroy()
                        showerror(title="Ошибка", message="Минимум не может быть больше максимума")
                    if min_exp < 0 or max_exp < 0:
                        window.destroy()
                        showerror(title="Ошибка", message="Минимум или максимум не может быть отрицательным")
                    conditions.append(lambda person: min_exp <= int(person[5]) <= max_exp)
                except ValueError:
                    pass  # Ignore invalid input for work experience range

            return conditions

        window = Tk()
        window.title("Удаление элемента")
        window.geometry("1200x400")
        window.resizable(False, False)
        frame = ttk.Frame(window, borderwidth=1, relief=SOLID, padding=[10, 10])

        # Извлечение данных из модели
        faculties = list(set([self.model.persons[i][0] for i in range(len(self.model.persons))]))
        departments = list(set([self.model.persons[i][1] for i in range(len(self.model.persons))]))
        snp = list(set([self.model.persons[i][2] for i in range(len(self.model.persons))]))
        academic_titles = list(set([self.model.persons[i][3] for i in range(len(self.model.persons))]))
        academic_degrees = list(set([self.model.persons[i][4] for i in range(len(self.model.persons))]))

        # Создание и настройка комбо-боксов и меток
        labels = ["Факультет", "Название кафедры", "ФИО преподавателя", "Ученое звание", "Ученая степень",
                  "Минимальный стаж работы", "Максимальный стаж работы"]
        comboboxes = [ttk.Combobox(frame) for _ in range(5)]  # 5 выпадающих списков, для стажа используем Entry

        # Размещение меток и комбо-боксов в grid
        for i, label in enumerate(labels[:5]):
            ttk.Label(frame, text=label).grid(row=0, column=i, padx=5, pady=5)
            comboboxes[i].grid(row=1, column=i, padx=5, pady=5, sticky="ew")

        comboboxes[0]['values'] = faculties
        comboboxes[1]['values'] = departments
        comboboxes[2]['values'] = snp
        comboboxes[3]['values'] = academic_titles
        comboboxes[4]['values'] = academic_degrees

        # Для стажа создаем поля ввода
        work_exp_min = ttk.Entry(frame)
        work_exp_max = ttk.Entry(frame)
        ttk.Label(frame, text=labels[5]).grid(row=0, column=5, padx=5, pady=5)
        work_exp_min.grid(row=1, column=5, padx=5, pady=5, sticky="ew")
        ttk.Label(frame, text=labels[6]).grid(row=0, column=6, padx=5, pady=5)
        work_exp_max.grid(row=1, column=6, padx=5, pady=5, sticky="ew")

        entries = comboboxes + [work_exp_min, work_exp_max]

        frame.grid(row=0, column=0, padx=10, pady=10, columnspan=7)

        def on_delete():
            conditions = create_conditions(entries)
            self.controller.delete_person_by_conditions(conditions)
            window.destroy()

        btn_delete = ttk.Button(window, text="Удалить", command=on_delete)
        btn_delete.grid(row=2, column=0, padx=10, pady=10, sticky="w", columnspan=7)
        window.mainloop()

    def search(self):
        def create_conditions(entries):
            conditions = []
            faculty, department, SNP, academic_title, academic_degree, work_exp_min, work_exp_max = entries

            if SNP.get():
                snp_parts = SNP.get().split()
                conditions.append(lambda person: any(part in person[2] for part in snp_parts))
            if department.get() and department.get() in departments:
                conditions.append(lambda person: person[1] == department.get())
            if academic_title.get() and academic_title.get() in academic_titles:
                conditions.append(lambda person: person[3] == academic_title.get())
            if academic_degree.get() and academic_degree.get() in academic_degrees:
                conditions.append(lambda person: person[4] == academic_degree.get())
            if faculty.get() and faculty.get() in faculties:
                conditions.append(lambda person: person[0] == faculty.get())
            if work_exp_min.get() and work_exp_max.get():
                min_exp = int(work_exp_min.get())
                max_exp = int(work_exp_max.get())
                if min_exp > max_exp:
                    showerror(title="Ошибка", message="Минимум не может быть больше максимума")
                    return None
                if min_exp < 0 or max_exp < 0:
                    showerror(title="Ошибка", message="Минимум или максимум не может быть отрицательным")
                    return None
                conditions.append(lambda person: min_exp <= int(person[5]) <= max_exp)

            return conditions

        window = Tk()
        window.title("Поиск элемента")
        window.geometry("1200x400")
        window.resizable(False, False)
        frame = ttk.Frame(window, borderwidth=1, relief=SOLID, padding=[10, 10])

        # Извлечение данных из модели
        faculties = list(set([self.model.persons[i][0] for i in range(len(self.model.persons))]))
        departments = list(set([self.model.persons[i][1] for i in range(len(self.model.persons))]))
        snp = list(set([self.model.persons[i][2] for i in range(len(self.model.persons))]))
        academic_titles = list(set([self.model.persons[i][3] for i in range(len(self.model.persons))]))
        academic_degrees = list(set([self.model.persons[i][4] for i in range(len(self.model.persons))]))

        # Создание и настройка комбо-боксов и меток
        labels = ["Факультет", "Название кафедры", "ФИО преподавателя", "Ученое звание", "Ученая степень",
                  "Минимальный стаж работы", "Максимальный стаж работы"]
        comboboxes = [ttk.Combobox(frame) for _ in range(5)]  # 5 выпадающих списков, для стажа используем Entry

        # Размещение меток и комбо-боксов в grid
        for i, label in enumerate(labels[:5]):
            ttk.Label(frame, text=label).grid(row=0, column=i, padx=5, pady=5)
            comboboxes[i].grid(row=1, column=i, padx=5, pady=5, sticky="ew")

        comboboxes[0]['values'] = faculties
        comboboxes[1]['values'] = departments
        comboboxes[2]['values'] = snp
        comboboxes[3]['values'] = academic_titles
        comboboxes[4]['values'] = academic_degrees

        # Для стажа создаем поля ввода
        work_exp_min = ttk.Entry(frame)
        work_exp_max = ttk.Entry(frame)
        ttk.Label(frame, text=labels[5]).grid(row=0, column=5, padx=5, pady=5)
        work_exp_min.grid(row=1, column=5, padx=5, pady=5, sticky="ew")
        ttk.Label(frame, text=labels[6]).grid(row=0, column=6, padx=5, pady=5)
        work_exp_max.grid(row=1, column=6, padx=5, pady=5, sticky="ew")

        entries = comboboxes + [work_exp_min, work_exp_max]

        frame.grid(row=0, column=0, padx=10, pady=10, columnspan=7)

        def on_search():
            conditions = create_conditions(entries)
            if conditions is None:
                return
            found_persons = self.controller.find_persons_by_conditions(conditions)
            self.display_found_persons(found_persons)
            self.file_menu.entryconfig("Сброс", state=NORMAL)  # Включаем кнопку сброса после поиска
            self.disable_menu_items()  # Отключаем все элементы меню
            window.destroy()

        btn_search = ttk.Button(window, text="Поиск", command=on_search)
        btn_search.grid(row=2, column=0, padx=10, pady=10, sticky="w", columnspan=3)

        window.mainloop()

    def display_found_persons(self, found_persons):
        self.controller.set_search_mode(True)
        self.controller.set_found_persons(found_persons)
        self.controller.first_page()  # Переключаемся на первую страницу результатов поиска

    def reset_search(self):
        self.controller.set_search_mode(False)
        self.update_table()
        self.file_menu.entryconfig("Сброс", state=DISABLED)  # Отключаем кнопку сброса после сброса
        self.enable_menu_items()  # Включаем все элементы меню

    def disable_menu_items(self):
        # Отключаем все элементы меню, кроме кнопки сброса
        menu_entries = self.file_menu.index("end")
        for index in range(menu_entries + 1):
            try:
                if self.file_menu.entrycget(index, "label") != "Сброс":
                    self.file_menu.entryconfig(index, state=DISABLED)
            except TclError:
                continue

    def enable_menu_items(self):
        # Включаем все элементы меню
        menu_entries = self.file_menu.index("end")
        for index in range(menu_entries + 1):
            try:
                self.file_menu.entryconfig(index, state=NORMAL)
                if self.file_menu.entrycget(index, "label") == "Сброс":
                    self.file_menu.entryconfig(index, state=DISABLED)
            except TclError:
                continue