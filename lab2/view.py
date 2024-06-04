import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
class BookRecord:
    def __init__(self,controller):
        self.master = tk.Tk()
        self.controller = controller
        self.int_var_for_volumes = tk.IntVar()
        self.int_var_for_editions = tk.IntVar()
        self.str_var_publisher = tk.StringVar()
        self.str_var_name = tk.StringVar()
        self.str_var_for_author = tk.StringVar()
        self.master.title("Учет книг")
        self.master.geometry('750x250')
        self.master.resizable(width=False,height = False)
        self.current_page = 0
        self.records_per_page = 5
        self._hz()

        
        
    

    def load_from_file(self):
        filename = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if filename:
            success = self.controller.load_records_from_xml(filename)
            if success:
                self.update_table()
            else:
                messagebox.showerror("Ошибка", "Не удалось загрузить данные из файла")
    def update_table(self):
        self.tree.delete(*self.tree.get_children())
        records = self.controller.get_records()
        start_index = self.current_page * self.records_per_page
        end_index = start_index + self.records_per_page
        for record in records[start_index:end_index]:
            self.tree.insert("", "end", values=record)
        self.update_pagination_buttons()

    def update_pagination_buttons(self):
        records = self.controller.get_records()
        if self.current_page == 0:
            self.prev_button.config(state=tk.DISABLED)
        else:
            self.prev_button.config(state=tk.NORMAL)
        if (self.current_page + 1) * self.records_per_page >= len(records):
            self.next_button.config(state=tk.DISABLED)
        else:
            self.next_button.config(state=tk.NORMAL)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_table()

    def next_page(self):
        if (self.current_page + 1) * self.records_per_page < len(self.controller.get_records()):
            self.current_page += 1
            self.update_table()



            
    def _main(self):
        self.master.mainloop()
        
    def _hz(self):
        button_frame = tk.Frame(self.master)
        button_frame.pack(anchor = 'nw')
        self.prev_button = tk.Button(button_frame, text="Предыдущая страница", command=self.prev_page)
        self.prev_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.next_button = tk.Button(button_frame, text="Следующая страница", command=self.next_page)
        self.next_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.load_button = tk.Button(button_frame, text="Загрузить из файла", command=self.load_from_file)
        self.load_button.pack(side='left',padx=5, pady=5)
        self.add_button = tk.Button(button_frame, text="Добавить запись", command=self.add_record)
        self.add_button.pack(side='left')

        self.delete_button = tk.Button(button_frame, text="Удалить запись", command=self.delete_record_dialog)
        self.delete_button.pack(side = 'left')

        self.find_button = tk.Button(button_frame, text="Найти запись",command = self.find_record)#, command=self.find_record
        self.find_button.pack(side = 'left',padx=(0,470))

        self.table_frame = tk.Frame(self.master)
        self.table_frame.pack(anchor = 'nw')

        columns = ("Название книги", "ФИО автора", "Издательство", "Число томов", "Тираж", "Итого томов")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        self.tree.heading("Название книги", text="Название книги")
        self.tree.heading("ФИО автора", text="ФИО автора")
        self.tree.heading("Издательство", text="Издательство")
        self.tree.heading("Число томов", text="Число томов")
        self.tree.heading("Тираж", text="Тираж")
        self.tree.heading("Итого томов", text="Итого томов")


        self.tree.column("Название книги", width=150)
        self.tree.column("ФИО автора", width=150)
        self.tree.column("Издательство", width=150)
        self.tree.column("Число томов", width=100)
        self.tree.column("Тираж", width=100)
        self.tree.column("Итого томов", width=100)


        self.tree.pack()

    def add_record(self):


        add_window = tk.Toplevel(self.master)
        add_window.title("Добавить запись")

        name_label = tk.Label(add_window, text="Название книги:")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(add_window,textvariable=self.str_var_name)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        author_label = tk.Label(add_window, text="ФИО автора:")
        author_label.grid(row=1, column=0, padx=5, pady=5)
        author_entry = tk.Entry(add_window,textvariable=self.str_var_for_author)
        author_entry.grid(row=1, column=1, padx=5, pady=5)

        publisher_label = tk.Label(add_window, text="Издательство:")
        publisher_label.grid(row=2, column=0, padx=5, pady=5)
        publisher_entry = tk.Entry(add_window,textvariable=self.str_var_publisher)
        publisher_entry.grid(row=2, column=1, padx=5, pady=5)

        volumes_label = tk.Label(add_window, text="Число томов:")
        volumes_label.grid(row=3, column=0, padx=5, pady=5)
        volumes_entry = tk.Entry(add_window,textvariable=self.int_var_for_volumes)
        volumes_entry.grid(row=3, column=1, padx=5, pady=5)

        edition_label = tk.Label(add_window, text="Тираж:")
        edition_label.grid(row=4, column=0, padx=5, pady=5)
        edition_entry = tk.Entry(add_window,textvariable=self.int_var_for_editions)
        edition_entry.grid(row=4, column=1, padx=5, pady=5)

        def get_add_record_info():
            name = name_entry.get()
            author = author_entry.get()
            publisher = publisher_entry.get()
            volumes = volumes_entry.get()
            edition = edition_entry.get()
            num_of_tomes = int(volumes) * int(edition)
            self.controller.get_record_add_info(name, author, publisher, volumes, edition,num_of_tomes)
        

            name, author, publisher, volumes, edition,num_of_tomes = self.controller.give_records_info()

            if not name or not author or not publisher or not volumes or not edition:
                messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
                return


            self.tree.insert("", tk.END, values=(name, author, publisher, volumes, edition, int(volumes) * int(edition)))
            self.update_table()

            add_window.destroy()
            return name,author,publisher,volumes,edition,num_of_tomes

        add_button = tk.Button(add_window, text="Добавить",command=get_add_record_info) #, command=add_to_table
        add_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)
        

    def delete_record_dialog(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Выберите критерий удаления")

        def open_delete_by_author_dialog():
            dialog.destroy()
            self.delete_by_author_dialog()

        def open_delete_by_publisher_author_dialog():
            dialog.destroy()
            self.delete_by_publisher_author_dialog()

        def open_delete_by_volumes_dialog():
            dialog.destroy()
            self.delete_by_volumes_dialog()

        def open_delete_by_book_name_dialog():
            dialog.destroy()
            self.delete_by_book_name_dialog()

        def open_delete_by_edition_dialog():
            dialog.destroy()
            self.delete_by_edition_dialog()

        def open_delete_by_total_volumes_dialog():
            dialog.destroy()
            self.delete_by_total_volumes_dialog()

        tk.Button(dialog, text="По автору", command=open_delete_by_author_dialog).pack(padx=20, pady=5)
        tk.Button(dialog, text="По издателю и автору", command=open_delete_by_publisher_author_dialog).pack(padx=20, pady=5)
        tk.Button(dialog, text="По числу томов", command=open_delete_by_volumes_dialog).pack(padx=20, pady=5)
        tk.Button(dialog, text="По названию книги", command=open_delete_by_book_name_dialog).pack(padx=20, pady=5)
        tk.Button(dialog, text="По тиражу", command=open_delete_by_edition_dialog).pack(padx=20, pady=5)
        tk.Button(dialog, text="По итогу томов", command=open_delete_by_total_volumes_dialog).pack(padx=20, pady=5)

    def delete_by_author_dialog(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Удалить по автору")

        author_label = tk.Label(dialog, text="ФИО автора:")
        author_label.pack(padx=5, pady=5)
        author_entry = tk.Entry(dialog)
        author_entry.pack(padx=5, pady=5)

        def delete_action():
            author = author_entry.get()
            self.controller.delete_by_author(author)
            dialog.destroy()
            self.update_table()

        delete_button = tk.Button(dialog, text="Удалить", command=delete_action)
        delete_button.pack(padx=5, pady=10)

    def delete_by_publisher_author_dialog(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Удалить по издателю и автору")

        publisher_label = tk.Label(dialog, text="Издательство:")
        publisher_label.pack(padx=5, pady=5)
        publisher_entry = tk.Entry(dialog)
        publisher_entry.pack(padx=5, pady=5)

        author_label = tk.Label(dialog, text="ФИО автора:")
        author_label.pack(padx=5, pady=5)
        author_entry = tk.Entry(dialog)
        author_entry.pack(padx=5, pady=5)

        def delete_action():
            publisher = publisher_entry.get()
            author = author_entry.get()
            self.controller.delete_by_publisher_and_author(publisher, author)
            dialog.destroy()
            self.update_table()


        delete_button = tk.Button(dialog, text="Удалить", command=delete_action)
        delete_button.pack(padx=5, pady=10)
        


    def delete_by_volumes_dialog(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Удалить по числу томов")

        min_volumes_label = tk.Label(dialog, text="Минимум томов:")
        min_volumes_label.pack(padx=5, pady=5)
        min_volumes_entry = tk.Entry(dialog)
        min_volumes_entry.pack(padx=5, pady=5)

        max_volumes_label = tk.Label(dialog, text="Максимум томов:")
        max_volumes_label.pack(padx=5, pady=5)
        max_volumes_entry = tk.Entry(dialog)
        max_volumes_entry.pack(padx=5, pady=5)

        def delete_action():
            min_volumes = int(min_volumes_entry.get())
            max_volumes = int(max_volumes_entry.get())
            self.controller.delete_by_volumes(min_volumes, max_volumes)
            dialog.destroy()
            self.update_table()

        delete_button = tk.Button(dialog, text="Удалить", command=delete_action)
        delete_button.pack(padx=5, pady=10)

    def show_search_results(self, results):
        self.tree.delete(*self.tree.get_children())  
        for record in results:
            self.tree.insert("", tk.END, values=record)  


    def delete_by_book_name_dialog(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Удалить по названию книги")

        book_name_label = tk.Label(dialog, text="Название книги:")
        book_name_label.pack(padx=5, pady=5)
        book_name_entry = tk.Entry(dialog)
        book_name_entry.pack(padx=5, pady=5)

        def delete_action():
            book_name = book_name_entry.get()
            self.controller.delete_by_book_name(book_name)
            dialog.destroy()
            self.update_table()

        delete_button = tk.Button(dialog, text="Удалить", command=delete_action)
        delete_button.pack(padx=5, pady=10)
        self.update_table()
        
    def delete_by_edition_dialog(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Удалить по тиражу")

        min_edition_label = tk.Label(dialog, text="Минимальный тираж:")
        min_edition_label.pack(padx=5, pady=5)
        min_edition_entry = tk.Entry(dialog)
        min_edition_entry.pack(padx=5, pady=5)

        max_edition_label = tk.Label(dialog, text="Максимальный тираж:")
        max_edition_label.pack(padx=5, pady=5)
        max_edition_entry = tk.Entry(dialog)
        max_edition_entry.pack(padx=5, pady=5)

        def delete_action():
            min_edition = int(min_edition_entry.get())
            max_edition = int(max_edition_entry.get())
            self.controller.delete_by_edition(min_edition, max_edition)
            dialog.destroy()
            self.update_table()

        delete_button = tk.Button(dialog, text="Удалить", command=delete_action)
        delete_button.pack(padx=5, pady=10)
    
    def delete_by_total_volumes_dialog(self):
        
        dialog = tk.Toplevel(self.master)
        dialog.title("Удалить по тиражу")
        min_edition_label = tk.Label(dialog, text="Минимально итого томов:")
        min_edition_label.pack(padx=5, pady=5)
        min_edition_entry = tk.Entry(dialog)
        min_edition_entry.pack(padx=5, pady=5)
        max_edition_label = tk.Label(dialog, text="Максимально итого томов")
        max_edition_label.pack(padx=5, pady=5)
        max_edition_entry = tk.Entry(dialog)
        max_edition_entry.pack(padx=5, pady=5)
        def delete_action():
            min_edition = int(min_edition_entry.get())
            max_edition = int(max_edition_entry.get())
            self.controller.delete_by_total_volumes(min_edition, max_edition)
            dialog.destroy()
            self.update_table()

        delete_button = tk.Button(dialog, text="Удалить", command=delete_action)
        delete_button.pack(padx=5, pady=10)
        
    def find_record(self):
        find_window = tk.Toplevel(self.master)
        find_window.title("Найти запись")

        criteria_label = tk.Label(find_window, text="Выберите критерий поиска:")
        criteria_label.pack(padx=5, pady=5)

        criteria = tk.StringVar(value="author")

        criteria_frame = tk.Frame(find_window)
        criteria_frame.pack(padx=5, pady=5)

        author_radio = tk.Radiobutton(criteria_frame, text="По автору", variable=criteria, value="author")
        author_radio.pack(anchor="w")

        publisher_author_radio = tk.Radiobutton(criteria_frame, text="По издательству и автору", variable=criteria, value="publisher_author")
        publisher_author_radio.pack(anchor="w")

        book_name_radio = tk.Radiobutton(criteria_frame, text="По названию книги", variable=criteria, value="book_name")
        book_name_radio.pack(anchor="w")

        volumes_radio = tk.Radiobutton(criteria_frame, text="По числу томов", variable=criteria, value="volumes")
        volumes_radio.pack(anchor="w")

        edition_radio = tk.Radiobutton(criteria_frame, text="По тиражу", variable=criteria, value="edition")
        edition_radio.pack(anchor="w")

        total_volumes_radio = tk.Radiobutton(criteria_frame, text="По итогу томов", variable=criteria, value="total_volumes")
        total_volumes_radio.pack(anchor="w")

        def search_action():
            criteria_value = criteria.get()
            self.open_search_criteria_window(criteria_value)
            find_window.destroy()

        search_button = tk.Button(find_window, text="Выбрать", command=search_action)
        search_button.pack(padx=5, pady=10)
    
    def open_search_criteria_window(self, criteria):
        search_window = tk.Toplevel(self.master)
        search_window.title("Введите критерий поиска")

        if criteria == "author":
            self.create_search_by_author_window(search_window)
        elif criteria == "publisher_author":
            self.create_search_by_publisher_author_window(search_window)
        elif criteria == "book_name":
            self.create_search_by_book_name_window(search_window)
        elif criteria == "volumes":
            self.create_search_by_volumes_window(search_window)
        elif criteria == "edition":
            self.create_search_by_edition_window(search_window)
        elif criteria == "total_volumes":
            self.create_search_by_total_volumes_window(search_window)
            
    def create_search_by_author_window(self, window):
        author_label = tk.Label(window, text="ФИО автора:")
        author_label.pack(padx=5, pady=5)
        author_entry = tk.Entry(window)
        author_entry.pack(padx=5, pady=5)

        def search_action():
            author = author_entry.get()
            self.show_search_results([record for record in self.controller.get_records() if record[1] == author])
            window.destroy()

        search_button = tk.Button(window, text="Поиск", command=search_action)
        search_button.pack(padx=5, pady=10)


    def create_search_by_publisher_author_window(self, window):
        publisher_label = tk.Label(window, text="Издательство:")
        publisher_label.pack(padx=5, pady=5)
        publisher_entry = tk.Entry(window)
        publisher_entry.pack(padx=5, pady=5)

        author_label = tk.Label(window, text="ФИО автора:")
        author_label.pack(padx=5, pady=5)
        author_entry = tk.Entry(window)
        author_entry.pack(padx=5, pady=5)

        def search_action():
            publisher = publisher_entry.get()
            author = author_entry.get()
            self.show_search_results([record for record in self.controller.get_records() if record[1] == author and record[2] == publisher])
            window.destroy()

        search_button = tk.Button(window, text="Поиск", command=search_action)
        search_button.pack(padx=5, pady=10)

    def create_search_by_book_name_window(self, window):
        book_name_label = tk.Label(window, text="Название книги:")
        book_name_label.pack(padx=5, pady=5)
        book_name_entry = tk.Entry(window)
        book_name_entry.pack(padx=5, pady=5)

        def search_action():
            book_name = book_name_entry.get()
            self.show_search_results([record for record in self.controller.get_records() if record[0] == book_name])
            window.destroy()

        search_button = tk.Button(window, text="Поиск", command=search_action)
        search_button.pack(padx=5, pady=10)

    def create_search_by_volumes_window(self, window):
        min_volumes_label = tk.Label(window, text="Минимальное число томов:")
        min_volumes_label.pack(padx=5, pady=5)
        min_volumes_entry = tk.Entry(window)
        min_volumes_entry.pack(padx=5, pady=5)

        max_volumes_label = tk.Label(window, text="Максимальное число томов:")
        max_volumes_label.pack(padx=5, pady=5)
        max_volumes_entry = tk.Entry(window)
        max_volumes_entry.pack(padx=5, pady=5)

        def search_action():
            min_volumes = int(min_volumes_entry.get())
            max_volumes = int(max_volumes_entry.get())
            self.show_search_results([record for record in self.controller.get_records() if min_volumes <= int(record[3]) <= max_volumes])
            window.destroy()

        search_button = tk.Button(window, text="Поиск", command=search_action)
        search_button.pack(padx=5, pady=10)

    def create_search_by_edition_window(self, window):
        min_edition_label = tk.Label(window, text="Минимальный тираж:")
        min_edition_label.pack(padx=5, pady=5)
        min_edition_entry = tk.Entry(window)
        min_edition_entry.pack(padx=5, pady=5)

        max_edition_label = tk.Label(window, text="Максимальный тираж:")
        max_edition_label.pack(padx=5, pady=5)
        max_edition_entry = tk.Entry(window)
        max_edition_entry.pack(padx=5, pady=5)

        def search_action():
            min_edition = int(min_edition_entry.get())
            max_edition = int(max_edition_entry.get())
            self.show_search_results([record for record in self.controller.get_records() if min_edition <= int(record[4]) <= max_edition])
            window.destroy()

        search_button = tk.Button(window, text="Поиск", command=search_action)
        search_button.pack(padx=5, pady=10)

    def create_search_by_total_volumes_window(self, window):
        min_total_volumes_label = tk.Label(window, text="Минимальное итого томов:")
        min_total_volumes_label.pack(padx=5, pady=5)
        min_total_volumes_entry = tk.Entry(window)
        min_total_volumes_entry.pack(padx=5, pady=5)

        max_total_volumes_label = tk.Label(window, text="Максимальное итого томов:")
        max_total_volumes_label.pack(padx=5, pady=5)
        max_total_volumes_entry = tk.Entry(window)
        max_total_volumes_entry.pack(padx=5, pady=5)

        def search_action():
            min_total_volumes = int(min_total_volumes_entry.get())
            max_total_volumes = int(max_total_volumes_entry.get())
            self.show_search_results([record for record in self.controller.get_records() if min_total_volumes <= int(record[5]) <= max_total_volumes])
            window.destroy()

        search_button = tk.Button(window, text="Поиск", command=search_action)
        search_button.pack(padx=5, pady=10)
        




