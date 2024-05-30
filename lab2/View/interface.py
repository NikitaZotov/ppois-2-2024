import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkcalendar import Calendar, DateEntry
import tkinter.messagebox
from typing import Any, Callable
from View.delete_interface import DeleteInterface
from View.search_interface import SearchInterface
from Model.database import Database
from Model.tournament import Tournament
from Controller.main_controller import MainController

search_list = ["Название турнира",
               "Дата проведения",
               "Название спорта",
               "Имя победителя",
               "Размер призового фонда",
               "Приз победителя", ]


class Interface:
    def __init__(self, controller: MainController):
        self.window = Tk()
        self.controller = controller
        #self.window.geometry("1280x1280")
        self.window.title("tournament")
        self.window.resizable(width=False, height=False)
        self.frame_table = Frame(self.window)
        # Таблица турнира
        colums = ("id", "name_tournament", "date", "name_sport", "name_winner", "prize_pool", "prize_winner")
        self.table = ttk.Treeview(self.frame_table, columns=colums, show="headings")
        for head in colums:
            self.table.column(head, anchor="center")
        self.table.heading("id", text="id")
        self.table.heading("name_tournament", text="Название турнира")
        self.table.heading("date", text="Дата проведения")
        self.table.heading("name_sport", text="Название спорта")
        self.table.heading("name_winner", text="Имя победителя")
        self.table.heading("prize_pool", text="Призовой фонд")
        self.table.heading("prize_winner", text="Приз победителя")
        self.tournament_list = self.get_data()
        self.current_page = 1
        self.size_page = 5
        self.max_page = (int(len(self.tournament_list) / self.size_page)
                         + bool((len(self.tournament_list) / self.size_page) % 1))
        example_list = [[0, 0, 1, 1, 1, 1, 1], [2, 1, 1, 1, 1, 1, 1]
                        , [3, 2, 1, 1, 1, 1, 1], [4, 3, 1, 1, 1, 1, 1]
                        , [5, 4, 1, 1, 1, 1, 1], [6, 5, 1, 1, 1, 1, 1], [7, 6, 1, 1, 1, 1, 1], [8, 7, 1, 1, 1, 1, 1]]
        for row in range(self.size_page):
            self.table.insert('', tk.END, values=self.tournament_list[row].data_format())
        self.first_page_btn = tk.Button(self.frame_table, text="<<", command=self.first_page)
        self.prev_page_btn = tk.Button(self.frame_table, text="<", command=self.prev_page)
        self.next_page_btn = tk.Button(self.frame_table, text=">", command=self.next_page)
        self.last_page_btn = tk.Button(self.frame_table, text=">>", command=self.last_page)
        self.page_text = tk.Label(self.frame_table, text=f"page {self.current_page} / {self.max_page}")
        self.page_number = tk.Entry(self.frame_table)
        self.number_elems = ttk.Combobox(self.frame_table, values=["5", "7", "9"])
        self.number_elems.current(0)
        self.number_elems.bind("<<ComboboxSelected>>", self.input_size_page)
        """self.number_text.grid(row=2, column=0)
        self.number_elems.grid(row=2, column=1)
        self.first_page_btn.grid(row=1, column=0)
        self.prev_page_btn.grid(row=1, column=1)
        self.page_text.grid(row=1, column=2)
        self.page_number.grid(row=1, column=3)
        self.next_page_btn.grid(row=1, column=4)
        self.last_page_btn.grid(row=1, column=5)
        self.table.grid(row=0, column=0, columnspan=1, pady=20, padx=25)"""
        self.table.pack(anchor="n")
        self.first_page_btn.pack(side="left")
        self.prev_page_btn.pack(side="left")
        self.next_page_btn.pack(side="left")
        self.last_page_btn.pack(side="left")
        self.number_elems.pack()
        self.page_text.pack()
        self.frame_table.grid(row=2, column=0, columnspan=5)
        # self.table.pack()
        # Окно добавления
        self.frame_add = Frame(self.window)
        self.entry_tournament_name = tk.Entry(self.frame_add)
        self.entry_date = DateEntry(self.frame_add, date_pattern="YYYY-mm-dd")
        self.entry_name_sport = tk.Entry(self.frame_add)
        self.entry_name_winner = tk.Entry(self.frame_add)
        check = (self.window.register(self.is_number), "%P")
        self.entry_prize_pool = tk.Entry(self.frame_add, validate="key", validatecommand=check)
        self.tournament_name_label = tk.Label(self.frame_add, text="Название турнира")
        self.date_label = tk.Label(self.frame_add, text="Дата проведения")
        self.name_sport_label = tk.Label(self.frame_add, text="Название спорта")
        self.name_winner_label = tk.Label(self.frame_add, text="Имя победителя")
        self.prize_pool_label = tk.Label(self.frame_add, text="Призовой фонд")
        self.add_btn = tk.Button(self.frame_add, text="Добавить турнир", command=self.add_button_click)
        self.entry_tournament_name.grid(row=0, column=0, sticky="w")
        self.entry_date.grid(row=1, column=0, sticky="w")
        self.entry_name_sport.grid(row=2, column=0, sticky="w")
        self.entry_name_winner.grid(row=3, column=0, sticky="w")
        self.entry_prize_pool.grid(row=4, column=0, sticky="w")
        self.tournament_name_label.grid(row=0, column=1, sticky="e")
        self.date_label.grid(row=1, column=1, sticky="e")
        self.name_sport_label.grid(row=2, column=1, sticky="e")
        self.name_winner_label.grid(row=3, column=1, sticky="e")
        self.prize_pool_label.grid(row=4, column=1, sticky="e")
        self.add_btn.grid(row=5, column=0, columnspan=2)
        self.frame_add.grid(row=1, column=0, sticky="w")
        """    self.entry_tournament_name.pack()
        self.entry_name_sport.pack()
        self.entry_name_winner.pack()
        self.entry_prize_pool.pack()
        self.add_btn.pack()"""
        self.frame_options = tk.Frame(self.window)
        # вызов окна удаления
        self.delete_btn = Button(self.frame_options, text="Удалить турнир", command=self.delete_button_click)

        # self.delete_btn.pack()
        # вызов окна поиска
        self.search_btn = Button(self.frame_options, text="Поиск турнира", command=self.search_button_click)

        # таблица выбора поиска/удаления
        self.choose_label = tk.Label(self.frame_options, text="Выбор поиска/удаления")
        self.choose_list_search = ttk.Combobox(self.frame_options, values=search_list)
        self.choose_list_search.current(0)
        self.choose_label.grid(row=1, column=0, columnspan=4)
        self.choose_list_search.grid(row=2, column=0, columnspan=4)
        self.frame_options.grid(row=3, column=0, columnspan=4)
        self.search_btn.grid(row=0, column=0)
        self.delete_btn.grid(row=0, column=1)
        self.frame_options.grid(row=1, column=1, columnspan=4, sticky="e")
        # self.search_btn.pack()
        self.window.mainloop()

    def is_number(self, number):

        try:
            float(number)
            return True
        except ValueError:
            if len(number) == 0:
                return True
            return False

    def delete_button_click(self):
        DeleteInterface(master=self.window, application=self,
                        type_delete=search_list.index(self.choose_list_search.get()))

    def search_button_click(self):
        SearchInterface(master=self.window, application=self,
                        type_search=search_list.index(self.choose_list_search.get()))

    def add_button_click(self):
        self.get_add_info()

    def get_data(self):
        return self.controller.get_all_tournaments()

    def get_add_info(self):
        if (len(self.entry_tournament_name.get()) == 0 or len(self.entry_name_sport.get()) == 0
            or len(self.entry_name_winner.get()) == 0 or len(self.entry_prize_pool.get()) == 0):
            tkinter.messagebox.showinfo(message=f"Незаполнены все поля")
            return None
        data = Tournament(self.entry_tournament_name.get(),
                          self.entry_date.get(),
                          self.entry_name_sport.get(),
                          self.entry_name_winner.get(),
                          float(self.entry_prize_pool.get()))
        res = self.controller.add_data(data)
        if res:
            tkinter.messagebox.showinfo(message=f"Успешно добавлен в базу данных")
            self.clear_entry()
            self.update_list()

    def input_size_page(self, event):
        self.size_page = int(self.number_elems.get())
        self.max_page = (int(len(self.tournament_list) / self.size_page)
                         + bool((len(self.tournament_list) / self.size_page) % 1))
        self.current_page = 1
        self.update_table()
        self.update_page_message()
        print(self.size_page)

    def update_table(self):
        for item in self.table.get_children():
            self.table.delete(item)
        new_page = self.tournament_list[(self.current_page-1)*self.size_page:min(len(self.tournament_list),
                                                                             self.current_page*self.size_page)]
        for item in new_page:
            self.table.insert('', tk.END, values=item.data_format())

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_table()
            self.update_page_message()

    def next_page(self):
        if self.current_page < self.max_page:
            self.current_page += 1
            self.update_table()
            self.update_page_message()

    def last_page(self):
        if self.current_page != self.max_page:
            self.current_page = self.max_page
            self.update_table()
            self.update_page_message()

    def first_page(self):
        if self.current_page != 1:
            self.current_page = 1
            self.update_table()
            self.update_page_message()

    def update_page_message(self):
        self.page_text.config(text=f"page {self.current_page} / {self.max_page}")

    def update_list(self):
        self.tournament_list = self.controller.get_all_tournaments()
        self.max_page = (int(len(self.tournament_list) / self.size_page)
                         + bool((len(self.tournament_list) / self.size_page) % 1))
        self.current_page = 1
        self.update_table()

    def clear_entry(self):
        self.entry_name_winner.delete(0, END)
        self.entry_tournament_name.delete(0, END)
        self.entry_prize_pool.delete(0, END)
        self.entry_name_sport.delete(0, END)

if __name__ == '__main__':
    model = None
    interface = Interface(model)
