import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

class View(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Система управления записями факультетов")
        self.geometry("1900x300")
        style = ThemedStyle(self)
        style.set_theme("plastik")
        self.records_per_page = 10
        self.current_page = 1

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Добавить запись", command=self.controller.show_add_dialog)
        self.file_menu.add_command(label="Выйти", command=self.quit)

        self.toolbar_frame = ttk.Frame(self)
        self.toolbar_frame.pack(side=tk.TOP, fill=tk.X)

        self.add_button = ttk.Button(self.toolbar_frame, text="Добавить запись",
                                     command=self.controller.show_add_dialog)
        self.add_button.pack(side=tk.LEFT)

        self.search_button = ttk.Button(self.toolbar_frame, text="Поиск", command=self.controller.show_search_dialog)
        self.search_button.pack(side=tk.LEFT)

        self.save_button = ttk.Button(self.toolbar_frame, text="Сохранить",
                                      command=self.controller.save_records_to_file)
        self.save_button.pack(padx=5, pady=5, side=tk.LEFT)

        self.load_button = ttk.Button(self.toolbar_frame, text="Загрузить",
                                      command=self.controller.load_records_from_file)
        self.load_button.pack(padx=5, pady=5, side=tk.LEFT)

        self.delete_button = ttk.Button(self.toolbar_frame, text="Удалить", command=self.controller.show_delete_dialog)
        self.delete_button.pack(padx=5, pady=5, side=tk.LEFT)

        self.records_frame = ttk.Frame(self)
        self.records_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.records_frame, columns=(
        "Факультет", "Название кафедры", "ФИО преподавателя", "Ученое звание", "Ученая степень", "Стаж работы"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("Факультет", text="Факультет")
        self.tree.heading("Название кафедры", text="Название кафедры")
        self.tree.heading("ФИО преподавателя", text="ФИО преподавателя")
        self.tree.heading("Ученое звание", text="Ученое звание")
        self.tree.heading("Ученая степень", text="Ученая степень")
        self.tree.heading("Стаж работы", text="Стаж работы")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.page_control_frame = ttk.Frame(self)
        self.page_control_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.first_button = ttk.Button(self.page_control_frame, text="<< First", command=self.controller.first_page)
        self.first_button.grid(row=0, column=0)

        self.prev_button = ttk.Button(self.page_control_frame, text="< Prev", command=self.controller.prev_page)
        self.prev_button.grid(row=0, column=1)

        self.page_label = ttk.Label(self.page_control_frame, text="Page: 1")
        self.page_label.grid(row=0, column=2)

        self.next_button = ttk.Button(self.page_control_frame, text="Next >", command=self.controller.next_page)
        self.next_button.grid(row=0, column=3)

        self.last_button = ttk.Button(self.page_control_frame, text="Last >>", command=self.controller.last_page)
        self.last_button.grid(row=0, column=4)

        # Добавление метки для отображения информации о записях
        self.records_info_label = ttk.Label(self.page_control_frame, text="Records 0-0 from 0")
        self.records_info_label.grid(row=0, column=5, padx=5)

    def update_records_list(self, records):
        self.tree.delete(*self.tree.get_children())
        for i, record in enumerate(records, start=1):
            self.tree.insert("", "end", text=str(i), values=(
            record.faculty, record.department, record.professor, record.rank, record.degree, record.experience))

    def update_page_info(self, total_pages, current_page):
        self.current_page = current_page  # Обновляем значение self.current_page
        self.page_label.config(text=f"Page: {current_page}/{total_pages}")

    def update_records_info(self):
        total_records = len(self.controller.records)
        total_pages = (total_records + self.records_per_page - 1) // self.records_per_page
        if self.current_page > total_pages:
            self.current_page = total_pages
        start_index = (self.current_page - 1) * self.records_per_page + 1
        end_index = min(self.current_page * self.records_per_page, total_records)
        self.page_label.config(text=f"Page: {self.current_page}/{total_pages}")
        self.records_info_label.config(text=f"Records {start_index}-{end_index} from {total_records}")

    def update_search_results_tree(self, search_results, tree):
        tree.delete(*tree.get_children())
        for i, record in enumerate(search_results, start=1):
            tree.insert("", "end", text=str(i), values=(
            record.faculty, record.department, record.professor, record.rank, record.degree, record.experience))
