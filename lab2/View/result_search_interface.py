import tkinter as tk
import tkinter.ttk as ttk
from tkcalendar import Calendar, DateEntry
from tkinter import *
from Model.tournament import Tournament


class ResultSearchInterface(tk.Toplevel):
    def __init__(self,master, application, result_list: list[Tournament]):
        super().__init__(master)
        self.result_list = result_list
        self.application = application
        self.controller = application.controller
        # search table
        self.frame_search_table = tk.Frame(self)
        colums = ("id", "name_tournament", "date", "name_sport", "name_winner", "prize_pool", "prize_winner")
        self.table = ttk.Treeview(self.frame_search_table, columns=colums, show="headings")
        self.table.heading("id", text="id")
        self.table.heading("name_tournament", text="название турнира")
        self.table.heading("date", text="дата проведения")
        self.table.heading("name_sport", text="название спорта")
        self.table.heading("name_winner", text="ФИО победителя")
        self.table.heading("prize_pool", text="призовой фонд")
        self.table.heading("prize_winner", text="приз победителя")
        self.first_page_btn = tk.Button(self.frame_search_table, text="<<", command=self.first_page)
        self.prev_page_btn = tk.Button(self.frame_search_table, text="<", command=self.prev_page)
        self.next_page_btn = tk.Button(self.frame_search_table, text=">", command=self.next_page)
        self.last_page_btn = tk.Button(self.frame_search_table, text=">>", command=self.last_page)
        self.current_page = 1
        self.size_page = 5
        self.max_page = int(len(self.result_list) / self.size_page)+bool((len(self.result_list) / self.size_page) % 1)
        for row in range(min(self.size_page, len(self.result_list))):
            self.table.insert('', tk.END, values=self.result_list[row].data_format())
        self.page_text = tk.Label(self.frame_search_table, text=f"page {self.current_page} / {self.max_page}")
        self.page_number = tk.Entry(self.frame_search_table)
        self.number_elems = ttk.Combobox(self.frame_search_table, values=["5", "7", "9"])
        self.number_elems.current(0)
        self.number_elems.bind("<<ComboboxSelected>>", self.input_size_page)
        # self.number_elems.current(0)
        self.table.pack(anchor="n")
        self.first_page_btn.pack(side="left")
        self.prev_page_btn.pack(side="left")
        self.next_page_btn.pack(side="left")
        self.last_page_btn.pack(side="left")
        self.number_elems.pack()
        self.page_text.pack()
        self.frame_search_table.grid(row=0, column=0, columnspan=4)

    def input_size_page(self, event):
        self.size_page = int(self.number_elems.get())
        self.max_page = int(len(self.result_list) / self.size_page)+bool((len(self.result_list) / self.size_page) % 1)
        self.current_page = 1
        self.update_table()
        self.update_page()

    def update_table(self):
        for item in self.table.get_children():
            self.table.delete(item)
        new_page = self.result_list[(self.current_page-1)*self.size_page:min(len(self.result_list),
                                                                             self.current_page*self.size_page)]
        for item in new_page:
            self.table.insert('', tk.END, values=item.data_format())

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_table()
            self.update_page()

    def next_page(self):
        if self.current_page < self.max_page:
            self.current_page += 1
            self.update_table()
            self.update_page()
    def last_page(self):
        if self.current_page != self.max_page:
            self.current_page = self.max_page
            self.update_table()
            self.update_page()

    def first_page(self):
        if self.current_page != 1:
            self.current_page = 1
            self.update_table()
            self.update_page()

    def update_page(self):
        self.page_text.config(text=f"page {self.current_page} / {self.max_page}")
