import tkinter as tk
import tkinter.ttk as ttk
from tkcalendar import Calendar, DateEntry
from View.result_search_interface import ResultSearchInterface
import tkinter.messagebox
import xml.etree.ElementTree
from tkinter import *
from Model.tournament import Tournament
from Controller.main_controller import MainController
search_list = ["Название турнира",
               "Дата проведения",
               "Название спорта",
               "Имя победителя",
               "Размер призового фонда",
               "Приз победителя", ]


class SearchInterface(tk.Toplevel):
    def __init__(self, master, application, type_search: int):
        super().__init__(master)
        self.application = application
        self.controller = application.controller
        self.type_search = type_search
        # search frame
        self.frame_search = tk.Frame(self)
        self.search_text = ""
        if self.type_search == 0 or self.type_search == 3:
            self.search_text = search_list[self.type_search]
            self.search_entry = ttk.Entry(self.frame_search)
            self.search_entry.grid(row=1, column=0)
        elif self.type_search == 2:
            self.search_text = search_list[self.type_search]
            self.search_entry = ttk.Combobox(self.frame_search, values=self.get_sports())
            self.search_entry.grid(row=1, column=0)
        elif self.type_search == 1:
            self.search_text = search_list[self.type_search]
            self.search_entry = DateEntry(self.frame_search, date_pattern="dd-mm-YYYY")
            self.search_entry.grid(row=1, column=0)
        elif 4 <= self.type_search <= 5:
            self.search_text = search_list[self.type_search]
            check = (self.master.register(self.is_number), "%P")
            self.search_label_min = tk.Label(self.frame_search, text="мин. значение")
            self.search_entry_min = ttk.Entry(self.frame_search, validate="key", validatecommand=check)
            self.search_label_min.grid(row=1, column=0)
            self.search_entry_min.grid(row=2, column=0)
            self.search_label_max = tk.Label(self.frame_search, text="макс. значение")
            self.search_entry_max = ttk.Entry(self.frame_search, validate="key", validatecommand=check)
            self.search_label_max.grid(row=1, column=1)
            self.search_entry_max.grid(row=2, column=1)
            print(search_list[self.type_search])
        self.search_btn = tk.Button(self.frame_search, text="Поиск", command=self.search_button)
        self.search_label = tk.Label(self.frame_search, text=self.search_text)
        self.search_label.grid(row=0, column=0)
        self.search_btn.grid(row=3, column=0)
        self.frame_search.grid(row=3, column=0)

    def is_number(self, number):
        try:
            float(number)
            return True
        except ValueError:
            if len(number) == 0:
                return True
            return False

    def search_button(self):
        if 4 <= self.type_search <= 5:
            if len(self.search_entry_max.get()) == 0 or len(self.search_entry_min.get()) == 0:
                tkinter.messagebox.showinfo(message=f"Незаполнены все поля")
                return None
            search_data_max = float(self.search_entry_max.get())
            search_data_min = float(self.search_entry_min.get())
            result = self.controller.search_data(self.type_search, search_data_min, second_elem=search_data_max)
        else:
            if len(self.search_entry.get()) == 0:
                tkinter.messagebox.showinfo(message=f"Незаполнены все поля")
                return None
            search_data = self.search_entry.get()
            print(search_data)
            result = self.controller.search_data(self.type_search, search_data)
        if len(result) > 0:
            ResultSearchInterface(self.master, self.application, result)
        else:
            tkinter.messagebox.showinfo(message=f"Ничего не найдено")
        self.destroy()

    def get_sports(self):
        return self.controller.get_sports()
