from tkinter import *
from tkinter import ttk
import xml.sax
from view.add_window import AddWindow
from view.search_window import SearchWindow
from view.delete_window import DeleteWindow
from tkinter import filedialog
from model.sax_parsers.all_criteries import PetAnyHandler,VetAnyHandler
from tkinter import messagebox
from xml.dom.minidom import Document


class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.table = ttk.Treeview(columns=("name", "birth_date", "last_visit_date",
                                           "vet_fio", "diagnosis"), show="headings")
        self.file_path = ''
        self.main_menu = Menu()
        self.file_menu = Menu(tearoff=0)
        self.string_menu = Menu(tearoff=0)
        self.inf_label = Label(text="Таблица информации")
        self.lists = Entry(self, width=10)
        self.current_page = 1
        self.rows_per_page = 10
        self.amount_pages = 1
        self.spinbox_val = IntVar(self, value=self.rows_per_page)
        self.placeholder = ''
        self.inf_label.pack()
        self.create_window()
        self.create_table()
        self.create_menu()
        self.create_navigation_buttons()
        self.create_lists()
        self.mainloop()

    def update_rows(self):
        self.rows_per_page = int(self.spinbox.get())
        self.show_first_page()
        self.find_amount_pages()
        self.update_placeholder()
        self.create_lists()

    def create_window(self):
        self.title("Ветклиника")
        self.geometry("1000x450")
        self.resizable(width=False, height=False)

    def create_menu(self):
        self.file_menu.add_command(label="Открыть", command=self.open_file)
        self.file_menu.add_command(label="Новый", command=self.new_file)
        self.string_menu.add_command(label="Добавить", command=self.start_add_window)
        self.string_menu.add_command(label="Найти", command=self.start_search_window)
        self.string_menu.add_command(label="Удалить", command=self.start_delete_window)
        self.main_menu.add_cascade(label="Файл", menu=self.file_menu)
        self.main_menu.add_cascade(label="Строка", menu=self.string_menu)
        self.config(menu=self.main_menu)

    def new_file(self):
        self.file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        if self.file_path:
            doc = Document()
            pet_records = doc.createElement("pet_records")
            doc.appendChild(pet_records)
            with open(self.file_path, "w", encoding="utf-8") as f:
                doc.writexml(f, indent="", addindent="  ", newl="\n", encoding="utf-8")
            messagebox.showinfo("Успех", f"Файл успешно создан: {self.file_path}")

    def create_table(self):
        self.table.heading("name", text="Имя", anchor=W)
        self.table.heading("birth_date", text="Дата рождения", anchor=W)
        self.table.heading("last_visit_date", text="Последний приём", anchor=W)
        self.table.heading("vet_fio", text="Ветеринар", anchor=W)
        self.table.heading("diagnosis", text="Диагноз", anchor=W)
        self.table.column("#1", stretch=TRUE, width=50)
        self.table.column("#2", stretch=TRUE, width=100)
        self.table.column("#3", stretch=TRUE, width=100)
        self.table.column("#4", stretch=TRUE, width=250)
        self.table.column("#5", stretch=TRUE, width=250)
        self.table.pack(fill=BOTH, expand=TRUE)

    def create_navigation_buttons(self):
        first_page_button = Button(self, text="<<", command=self.show_first_page)
        first_page_button.pack(side=LEFT)
        prev_page_button = Button(self, text="<", command=self.show_previous_page)
        prev_page_button.pack(side=LEFT)
        self.create_lists()
        next_page_button = Button(self, text=">", command=self.show_next_page)
        next_page_button.pack(side=LEFT)
        last_page_button = Button(self, text=">>", command=self.show_last_page)
        last_page_button.pack(side=LEFT)
        spinbox_label = Label(text="Количество строк: ")
        spinbox_label.pack(side=LEFT)
        self.spinbox = Spinbox(from_=1, to=15, textvariable=self.spinbox_val, command=self.update_rows, width=5)
        self.spinbox.pack(side=LEFT)

    def show_previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_placeholder()

    def show_input_page(self, event):
        input_page = int(self.lists.get())
        if 0 < input_page <= self.amount_pages:
            self.current_page = input_page
            self.update_placeholder()

    def find_amount_pages(self):
        self.amount_pages = len(self.rows) // self.rows_per_page + (len(self.rows) % self.rows_per_page > 0)
        self.placeholder = f'{self.current_page} из {self.amount_pages}'

    def show_next_page(self):
        if self.current_page < self.amount_pages:
            self.current_page += 1
            self.update_placeholder()

    def show_first_page(self):
        self.current_page = 1
        self.update_placeholder()

    def show_last_page(self):
        self.current_page = self.amount_pages
        self.update_placeholder()

    def read_file(self):
        try:
            self.rows.clear()
            pet_parser = xml.sax.make_parser()
            pet_handler = PetAnyHandler()
            pet_parser.setContentHandler(pet_handler)
            pet_parser.parse(self.file_path)
            vet_parser = xml.sax.make_parser()
            vet_handler = VetAnyHandler()
            vet_parser.setContentHandler(vet_handler)
            vet_parser.parse(self.file_path)
            for i, (pet, vet) in enumerate(zip(pet_handler.result, vet_handler.result), start=1):
                pet_info = (pet["name"], pet["birth_date"], pet["last_visit_date"], vet["fio"], pet["diagnosis"])
                self.rows.append(pet_info)
        except ValueError:
            print("Ошибка работы с файлом")

    def load_data(self):
        self.find_amount_pages()
        start_index = (self.current_page - 1) * self.rows_per_page
        end_index = start_index + self.rows_per_page

        for item in self.rows[start_index:end_index]:
            self.table.insert("", END, values=item)

    def erase(self, event=None):
        if self.lists.get() == self.placeholder:
            self.lists.delete(0, 'end')

    def add(self, event=None):
        if self.lists.get() != self.placeholder:
            self.lists.delete(0, 'end')
            self.lists.insert(0, self.placeholder)
            self.focus_set()

    def create_lists(self):
        self.lists.pack(side=LEFT)
        self.add()
        self.lists.bind('<FocusIn>', self.erase)
        self.lists.bind('<FocusOut>', self.add)
        self.lists.bind("<Return>", self.show_input_page)

    def update_placeholder(self):
        self.erase()
        self.placeholder = f'{self.current_page} из {self.amount_pages}'
        self.table.delete(*self.table.get_children())
        self.load_data()
        self.add()

    def start_add_window(self):
        self.add_window = AddWindow(self.file_path)
        self.add_window.mainloop()
        self.read_file()
        self.update_placeholder()

    def start_search_window(self):
        self.search_window = SearchWindow(self)
        self.search_window.mainloop()

    def start_delete_window(self):
        self.delete_window = DeleteWindow(self)
        self.delete_window.mainloop()
        self.read_file()
        self.update_placeholder()

    def open_file(self):
        self.file_path = filedialog.askopenfilename()
        try:
            self.read_file()
            self.update_placeholder()
        except xml.sax._exceptions.SAXParseException:
            self.file_path = ''
            messagebox.showerror("Ошибка", "Открывайте файлы с расширением xml")
