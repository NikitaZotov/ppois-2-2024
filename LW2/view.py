from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning
from model import Model
from controller import Controller


class View:
    def __init__(self, model: Model, controller: Controller):
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
        self.update_table()

    def update_table(self):
        # Очищаем таблицу перед добавлением новых данных
        for item in self.table.get_children():
            self.table.delete(item)

        # Добавляем все персоны из модели
        for person in self.model.persons:
            self.table.insert("", "end", values=person)

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
        self.file_menu.add_command(label="Добавить эл-нт", command= self.add_element)
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
                try:
                    min_exp = int(work_exp_min.get())
                    max_exp = int(work_exp_max.get())
                    conditions.append(lambda person: min_exp <= int(person[5]) <= max_exp)
                except ValueError:
                    pass  # Ignore invalid input for work experience range

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
            found_persons = self.controller.find_persons_by_conditions(conditions)
            self.display_found_persons(found_persons)
            self.file_menu.entryconfig("Сброс", state=NORMAL)  # Включаем кнопку сброса после поиска
            self.disable_menu_items()  # Отключаем все элементы меню
            window.destroy()

        btn_search = ttk.Button(window, text="Поиск", command=on_search)
        btn_search.grid(row=2, column=0, padx=10, pady=10, sticky="w", columnspan=3)

        window.mainloop()

    def display_found_persons(self, found_persons):
        # Очищаем таблицу перед добавлением новых данных
        for item in self.table.get_children():
            self.table.delete(item)

        # Добавляем найденные персоны в таблицу
        for index in found_persons:
            person = self.model.persons[index]
            self.table.insert("", "end", values=person)

    def reset_search(self):
        self.controller.reset_search()
        self.update_table()
        self.file_menu.entryconfig("Сброс", state=DISABLED)  # Отключаем кнопку сброса после сброса
        self.enable_menu_items()  # Включаем все элементы меню

    def disable_menu_items(self):
        # Отключаем все элементы меню, кроме кнопки сброса
        menu_entries = self.file_menu.index("end")
        for index in range(menu_entries + 1):
            if self.file_menu.entrycget(index, "label") != "Сброс":
                self.file_menu.entryconfig(index, state=DISABLED)

    def enable_menu_items(self):
        # Включаем все элементы меню
        menu_entries = self.file_menu.index("end")
        for index in range(menu_entries + 1):
            self.file_menu.entryconfig(index, state=NORMAL)